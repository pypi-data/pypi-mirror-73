# -*- coding: utf-8 -*-
# Copyright (c) 2016 - 2020 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#
""" Execute and sanitize remote commands
"""
import json
import logging
from copy import copy
from itertools import groupby
from operator import itemgetter

from sqreen.performance_metrics import PerformanceMetricsSettings

from . import config
from .rules_callbacks import cb_from_rule
from .runtime_storage import runtime
from .sdk.events import STACKTRACE_EVENTS
from .signature import RSAVerifier

LOGGER = logging.getLogger(__name__)


class RemoteCommand(object):
    """ Class responsible for dispatching and executing remote commands
    """

    def __init__(self):
        self.commands = {}
        self.coalesce = set()

    def register_command(self, command_name, command, coalesce=False):
        """ Register a command callback for command name
        """
        self.commands[command_name] = command
        if coalesce:
            self.coalesce.add(command_name)

    def process_list(self, commands, *args, **kwargs):
        """ Process a list of command and assemble the result
        """
        res = {}
        if not isinstance(commands, list):
            LOGGER.debug(
                "Wrong commands type %s: %r", type(commands), commands
            )
            return res

        it = self.coalesce_commands(self.validate_commands(commands, res), res)
        for command in it:
            LOGGER.debug("Processing command %s", command["name"])

            # Command params
            command_params = command.get("params", [])

            # Then execute the command
            result = self.commands[command["name"]](
                *args, params=command_params, **kwargs
            )
            res[command["uuid"]] = self._format_result(result)

        return res

    def validate_commands(self, commands, results):
        """ Generator checking the commands have been registered.
        """
        for command in commands:
            uuid = command.get("uuid")
            if uuid is None:
                LOGGER.debug("skipping command without uuid: %r", command)
                continue
            name = command.get("name")
            if name not in self.commands:
                results[uuid] = {
                    "status": False,
                    "msg": "unknown command name {}".format(repr(name))
                }
                continue
            yield command

    def coalesce_commands(self, commands, results):
        """ Generator removing all duplicate adjacent commands.
        """
        for command_name, command_group in groupby(commands, itemgetter("name")):
            if command_name in self.coalesce:
                command_group = list(command_group)
                # Only keep the last command
                while len(command_group) > 1:
                    command = command_group.pop(0)
                    results[command["uuid"]] = {
                        "status": False,
                        "reason": "skipped duplicate {}".format(command_name)
                    }
            for command in command_group:
                yield command

    def process(self, command, *args, **kwargs):
        """ Process a single command (deprecated, only used by the PHP Daemon).
        """
        return self.process_list([command], *args, **kwargs).popitem()[1]

    @staticmethod
    def _format_result(result):
        """ Format the command result for the backend
        """
        if result is None:
            return {"status": False, "output": "None returned"}
        elif result is True:
            return {"status": True}
        else:
            return {"status": True, "output": result}

    @classmethod
    def with_production_commands(cls):
        """ Returns a RemoteCommand with all production commands
        already registered
        """
        remote_command = cls()

        for name, command in ALL_COMMANDS.items():
            remote_command.register_command(name, command,
                                            coalesce=name in COALESCE_COMMANDS)

        return remote_command


###
# COMMANDS DEFINITION
###


def _load_local_rules():
    config_value = config.CONFIG["RULES"]
    if not config_value:
        return []
    with open(config_value) as rules_file:
        local_rules = json.load(rules_file)
    if not isinstance(local_rules, list):  # Single rule.
        local_rules = [local_rules]
    for rule_dict in local_rules:
        rule_dict["rulespack_id"] = "local"
    return local_rules


def _load_rules(runner, params=None, check_signature=True, storage=runtime):
    """ Retrieve the rulespack and instantiate the callbacks, returns
    a list of callbacks
    """
    rulespack_id, rules = None, None
    # Try to load rules and rulespack from params
    if params:
        try:
            rulespack_id, rules = params
        except ValueError:
            pass

    if rulespack_id is None or rules is None:
        rulespack = runner.session.get_rulespack()
        if rulespack is not None:
            rulespack_id = rulespack.get("pack_id")
            rules = rulespack.get("rules", [])

    if rules is None or len(rules) == 0 or rulespack_id is None:
        return None, []

    # Set the pack id on each rule
    for rule_dict in rules:
        rule_dict["rulespack_id"] = rulespack_id

    rules.extend(_load_local_rules())

    LOGGER.info("Retrieved rulespack id: %s", rulespack_id)
    rules_name = ", ".join(rule["name"] for rule in rules)
    LOGGER.debug("Retrieved %d rules: %s", len(rules), rules_name)

    # Check the rule signature only if the config say so
    if check_signature and config.CONFIG["RULES_SIGNATURE"] is True:
        verifier = RSAVerifier()
    else:
        verifier = None

    # Create the callbacks
    callbacks = []
    for rule_dict in rules:
        # Instantiate the rule callback
        callback = cb_from_rule(rule_dict, runner, verifier, storage=storage)

        # Check if the rule has some metrics to register
        for metric in rule_dict.get("metrics", []):
            runner.metrics_store.register_metric(**metric)

        if callback:
            LOGGER.debug(
                'Rule "%s" will hook on "%s %s" with callback %s with strategy %s',
                callback.rule_name,
                callback.hook_module,
                callback.hook_name,
                callback,
                callback.strategy,
            )

            callbacks.append(callback)

    return rulespack_id, callbacks


def _instrument_callbacks(runner, callbacks):
    """ For a given list of callbacks, hook them
    """
    # Clean existing callbacks to avoid double-instrumentation
    instrumentation_remove(runner)
    LOGGER.info("Setup instrumentation")
    for callback in callbacks:
        runner.instrumentation.add_callback(callback)
    runner.instrumentation.hook_all()


def instrumentation_enable(runner, params=None):
    """ Retrieve a rulespack, instantiate RuleCallback from the rules
    and instrument them.
    """
    # Load rules
    pack_id, rules = _load_rules(runner, params)

    if pack_id is None:
        LOGGER.debug("Couldn't get a valid rulespack, instrumentation is disabled")
        return None

    LOGGER.debug("Start instrumentation with rulespack %r", pack_id)
    # Instrument retrieved rules
    _instrument_callbacks(runner, rules)

    return pack_id


def instrumentation_remove(runner, params=None):
    """ Remove all callbacks from instrumentation, return True
    """
    LOGGER.info("Remove current instrumentation")
    runner.instrumentation.deinstrument_all()
    return True


def get_bundle(runner, params=None):
    """ Returns the list of installed Python dependencies
    """

    return {"status": runner.session.post_bundle(runner.runtime_infos) is not None}


def rules_reload(runner, params=None):
    """ Load the rules, deinstrument the old ones and instrument
    the new loaded rules. Returns the new rulespack_id
    """
    pack_id, rules = _load_rules(runner)
    if pack_id is None:
        LOGGER.debug("Couldn't get a valid rulespack, instrumentation not reloaded")
        return ""

    LOGGER.debug("Reloading instrumentation with rulespack %r", pack_id)
    # Reinstrument with the new rules
    _instrument_callbacks(runner, rules)

    return pack_id


def actions_reload(runner, params=None):
    """Remove old security actions and load the new ones."""
    LOGGER.debug("Reloading actions")
    data = runner.session.get_actionspack()
    if data["status"] is not True:
        LOGGER.debug("Cannot reload actions")
        return ""

    actions = data["actions"]
    LOGGER.debug("Reloading actions %s", actions)

    unsupported = runner.action_store.reload_from_dicts(actions or [])
    if unsupported:
        return {
            "status": False,
            "output": {"unsupported_actions": unsupported},
        }
    else:
        return {"status": True}


def record_stacktrace(runner, params=None):
    """Collect stacktraces for the given events."""
    STACKTRACE_EVENTS.clear()
    if params:
        LOGGER.debug("Collect stacktraces for events %r", params)
        STACKTRACE_EVENTS.update(params)
    else:
        LOGGER.debug("Don't collect any stacktrace event")
    return {"status": True}


def features_get(runner, params=None):
    return runner.features_get()


def features_change(runner, params):

    old_features = copy(runner.features_get())

    if len(params) != 1:
        raise ValueError("Invalid params list %s" % params)
    params = params[0]

    runner.set_performance_metrics_settings(
        PerformanceMetricsSettings.from_features(params))

    # Heartbeat delay only if we have a new value for it > 0
    heartbeat_delay = params.get("heartbeat_delay", 0)
    if heartbeat_delay > 0:
        runner.set_heartbeat_delay(heartbeat_delay)

    # Always set the new value of call_counts_metrics_period
    runner.set_call_counts_metrics_period(
        params.get("call_counts_metrics_period", 60)
    )

    # Always set the new value of whitelisted_metric
    runner.set_whitelisted_metric(params.get("whitelisted_metric", True))

    # Alter the deliverer if the batch_size is set
    if params.get("batch_size") is not None:
        runner.set_deliverer(
            params["batch_size"], params.get("max_staleness", 0),
            use_signals=params.get("use_signals", False)
        )

    new_features = copy(runner.features_get())

    return {"old": old_features, "now": new_features}


def performance_budget(runner, params):

    if len(params) == 0:
        params = [None]
    elif len(params) > 1:
        raise ValueError("Expected 1 or 0 items in list %s" % params)

    old_value = runner.budget
    runner.set_performance_cap_budget(params[0] or None)

    return {
        "status": True,
        "output": {"was": old_value}
    }


def ips_whitelist(runner, params):
    """ Replace current list of whitelisted IP networks
    """
    params = params[0]
    runner.set_ips_whitelist(params)
    return {"status": True}


def paths_whitelist(runner, params):
    """ Replace current list of whitelisted paths
    """
    params = params[0]

    runner.set_paths_whitelist(params)
    return {"status": True}


def force_logout(runner, params=None):
    instrumentation_remove(runner)
    runner.logout()
    return {"status": True}


ALL_COMMANDS = {
    "instrumentation_enable": instrumentation_enable,
    "instrumentation_remove": instrumentation_remove,
    "get_bundle": get_bundle,
    "rules_reload": rules_reload,
    "features_get": features_get,
    "features_change": features_change,
    "ips_whitelist": ips_whitelist,
    "paths_whitelist": paths_whitelist,
    "performance_budget": performance_budget,
    "force_logout": force_logout,
    "actions_reload": actions_reload,
    "record_stacktrace": record_stacktrace,
}
COALESCE_COMMANDS = ("actions_reload", "rules_reload",)
