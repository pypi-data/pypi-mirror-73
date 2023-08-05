# -*- coding: utf-8 -*-
# Copyright (c) 2016 - 2020 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#
""" DBApi2 strategy and custom connection and cursor classes
"""
import functools
import logging

from ..._vendors.wrapt import FunctionWrapper, ObjectProxy
from ..hook_point import hook_point
from .base import BaseStrategy

LOGGER = logging.getLogger(__name__)


class CustomCursor(ObjectProxy):
    """ CustomCursor proxy, it proxy a real Cursor of a DBApi2
    module, instrument all known DBApi2 methods.
    """

    __slots__ = ("callproc", "execute", "executemany", "executescript",
                 "close", "fetchone", "fetchmany", "fetchall", "nextstep",
                 "setinputsize", "setoutputsize")

    def __init__(self, real_cursor, hook_point, module_path):
        super(CustomCursor, self).__init__(real_cursor)
        hook_module = "{}::Cursor".format(module_path)

        for method_name in self.__slots__:
            method = getattr(self.__wrapped__, method_name, None)
            if method is not None:
                new_hook_point = hook_point(hook_module, method_name, method)
                setattr(self, method_name, new_hook_point)


class CustomConnection(ObjectProxy):
    """ CustomConnection proxy, it proxy a real Connection of a DBApi2
    module, instrument all DBApi2 known methods and returns
    CustomCursor when callin the cursor method.
    """

    __slots__ = ("execute", "executemany", "executescript", "close", "commit", "rollback")

    def __init__(self, real_connection, hook_point, module_path):
        super(CustomConnection, self).__init__(real_connection)
        self._self_sqreen_hook_point = hook_point
        self._self_sqreen_module_path = module_path
        hook_module = "{}::Connection".format(module_path)

        for method_name in self.__slots__:
            method = getattr(self.__wrapped__, method_name, None)
            if method is not None:
                new_hook_point = hook_point(hook_module, method_name, method)
                setattr(self, method_name, new_hook_point)

    def cursor(self, *args, **kwargs):
        """ Instantiate a real cursor, proxy it via CustomCursor.
        """
        return CustomCursor(
            self.__wrapped__.cursor(*args, **kwargs),
            self._self_sqreen_hook_point,
            self._self_sqreen_module_path,
        )


def custom_connect(hook_point, module_path, original_connect):
    """ Replacement to the connect function of a DBApi2 module. It will
    instantiate a connection via the original connect function and proxy it
    via CustomConnection defined earlier.
    """
    def wrapper(wrapped, instance, args, kwargs):
        return CustomConnection(
            wrapped(*args, **kwargs), hook_point, module_path)

    return FunctionWrapper(original_connect, wrapper)


class DBApi2Strategy(BaseStrategy):
    """ Strategy for DBApi2 drivers.

    It's different from the SetAttrStrategy and requires special care in
    hook_module and hook_name.
    DBApi2 tries to hook on 'connect' method of DBApi2 compatible driver.
    In order to do so, it needs the module name where 'connect' is available. It
    must be the first part of hook_module, for example in sqlite3, it will be
    'sqlite3'.

    The hook_module could then contains either '::Cursor' for hooking on
    cursor methods or '::Connection' for hooking on connection methods.
    The hook_name will then specify which method it will hook on.

    For example with sqlite3, the tuple ('sqlite3::Connection', 'execute') will
    reference the execute method on a sqlite3 connection.
    In the same way, the tuple ('sqlite3::Cursor', 'execute') will reference
    the execute method on a sqlite3 cursor.

    It will works the same way for all DBApi2 drivers, even with psycopg2
    where cursor class is actually defined as 'psycopg2.extensions.cursor',
    'psycopg2::Cursor' will correctly reference all psycopg2 cursor methods.
    """

    def __init__(
        self,
        module_path,
        observation_queue,
        queue,
        import_hook,
        before_hook_point=None,
    ):
        super(DBApi2Strategy, self).__init__(
            observation_queue, queue, import_hook, before_hook_point
        )
        self.module_path = module_path

        self.hooked = False

    def hook(self):
        """ Accept a callback and store it. If it's the first callback
        for this strategy, actually hook to the endpoint.

        Once hooked, it will instrument all method on connection and cursor.
        But if no callback is defined on a specific method, the overhead will
        be minimal.
        """
        # Check if we already hooked at
        if not self.hooked:
            self.import_hook.register_patcher(
                self.module_path, None, "connect", self.import_hook_callback
            )

            self.hooked = True

    def import_hook_callback(self, original):
        """ Monkey-patch the object located at hook_class.hook_name on an
        already loaded module
        """
        _hook_point = functools.partial(hook_point, self)
        return custom_connect(_hook_point, self.module_path, original)

    @staticmethod
    def get_strategy_id(callback):
        """ Returns the module part of hook_module (without everything after
        ::) as identifier for this strategy. Multiple hooks on sqlite3* should
        be done in this strategy.
        """
        # Check if the klass is part module and part klass name
        if "::" in callback.hook_module:
            return callback.hook_module.split("::", 1)[0]
        else:
            return callback.hook_module

    def _restore(self):
        """ The hooked module will always stay hooked
        """
        pass
