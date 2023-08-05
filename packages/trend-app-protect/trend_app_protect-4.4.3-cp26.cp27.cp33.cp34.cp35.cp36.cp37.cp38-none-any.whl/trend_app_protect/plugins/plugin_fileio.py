from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import os
import sys

from trend_app_protect.compat import get_builtins
from trend_app_protect.context import get_context
from trend_app_protect.logger import log
from trend_app_protect.patcher import monkeypatch

# Set plugin name so it can be enabled and disabled.
NAME = "file_io"
HOOKS_CALLED = ["file_io"]


def add_hooks(run_hook, get_agent_func=None, timer=None):
    """
    Add any OS hooks.
    """
    meta = {
        "version": ".".join(map(str, sys.version_info[:3])),  # Py version
    }

    # Define helper to check if FileIO is disabled. Used as the value for
    # `skip_if` parameter to the `@monkeypatch` decorator.
    def fileio_disabled():
        """
        Returns `True` if FileIO is disabled. Note the inverted logic!
        """
        if get_agent_func is None:
            # If we don't have a get_agent_func(), it means we're running in
            # a test environment, so leave FileIO enabled to ensure the hooks
            # run during the tests.
            return False
        agent = get_agent_func(create_if_required=False)
        if agent is None:
            # If the `get_agent_func()` is provided, but the Agent hasn't been
            # created yet, don't run the hooks.
            return True
        # If we do have an Agent, Check if `File Access` is enabled and invert
        # the logic value.
        return not agent.is_feature_enabled("File Access")

    hook_os_open(run_hook, timer, fileio_disabled)
    hook_builtin_open(run_hook, timer, fileio_disabled)

    return meta


def hook_os_open(run_hook, timer, fileio_disabled):
    """
    Add our hook into os.open
    """
    # Replace the original 'os.open'
    @monkeypatch(os, "open", timer=timer,
                 report_name="plugin.fileio.os_open",
                 skip_if=fileio_disabled)
    def _open(orig, *args, **kwargs):
        log.debug("os.open(%(args)s, %(kwargs)s)", {
            "args": args,
            "kwargs": kwargs,
        })

        try:
            if len(args) >= 2:
                filename = str(args[0])
                flags = args[1]
            elif len(args) >= 1:
                filename = str(args[0])
                flags = kwargs['flags']
            else:
                filename = str(kwargs['path'])
                flags = kwargs['flags']
            # ignore non-mode flags
            flags = flags & (os.O_RDWR | os.O_RDONLY | os.O_WRONLY)
        except Exception as e:
            log.warning("os.open unable to get params: " + str(e))
        else:
            # Send hook
            stack = get_context()
            run_hook("file_io", {
                "method": "os.open",
                "parameters": (filename, flags),
                "stack": stack,
                "cwd": os.getcwd()
            })
        return orig(*args, **kwargs)


def hook_builtin_open(run_hook, timer, fileio_disabled):
    """
    Add our hook into open.
    """
    builtin_module = get_builtins()

    # Replace the original 'open'
    @monkeypatch(builtin_module, "open", timer=timer,
                 report_name="plugin.fileio.builtin_open",
                 skip_if=fileio_disabled)
    def _open(orig, *args, **kwargs):
        log.debug("open(%(args)s, %(kwargs)s)", {
            "args": args,
            "kwargs": kwargs,
        })
        try:
            if len(args) >= 1:
                filename = str(args[0])

            if len(args) >= 2:
                mode = args[1]
            else:
                # Try from kwargs
                try:
                    mode = kwargs['mode']
                except KeyError:
                    mode = 'r'
        except Exception as e:
            log.warning("open unable to get params: " + str(e))
        else:
            # Send hook
            stack = get_context()
            run_hook("file_io", {
                "method": "open",
                "parameters": (filename, mode),
                "stack": stack,
                "cwd": os.getcwd(),
            })
        return orig(*args, **kwargs)
