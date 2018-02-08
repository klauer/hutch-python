import os
import sys
import argparse

from IPython.terminal.embed import (InteractiveShellEmbed,
                                    load_default_config)

from .ipython_log import init_ipython_logger
from .load_conf import load
from .log_setup import (setup_logging, set_console_level, debug_mode,
                        debug_context, debug_wrapper)
from .plugins import hutch


def setup_cli_env():
    # Parse the user's arguments
    parser = argparse.ArgumentParser(description='Launch LCLS Hutch Python')
    parser.add_argument('--cfg', required=True,
                        help='Configuration yaml file')
    parser.add_argument('--db', required=True,
                        help='Device database access information')
    parser.add_argument('--debug', action='store_true', default=False,
                        help='Start in debug mode')
    args = parser.parse_args()

    # Make sure the hutch's directory is in the path
    sys.path.insert(0, os.getcwd())

    # Set up logging first
    log_dir = os.path.join(os.path.dirname(args.cfg), 'logs')
    setup_logging(dir_logs=log_dir)

    # Debug mode second
    if args.debug:
        debug_mode(True)

    # Set the happi db path
    hutch.HAPPI_DB = args.db

    # Load objects from the configuration file
    objs = load(args.cfg)

    # Add cli debug tools
    objs['_debug_console_level'] = set_console_level
    objs['_debug_mode'] = debug_mode
    objs['_debug_context'] = debug_context
    objs['_debug_wrapper'] = debug_wrapper

    return objs


def hutch_ipython_embed():
    """
    This is very hacky, but I couldn't find a better way to adjust the shell
    from a call to embed.
    """
    config = load_default_config()
    config.InteractiveShellEmbed = config.TerminalInteractiveShell
    frame = sys._getframe(1)
    shell = InteractiveShellEmbed.instance(_init_location_id='%s:%s' % (
        frame.f_code.co_filename, frame.f_lineno), config=config)
    init_ipython_logger(shell)
    shell(header=u'', stack_depth=2, compile_flags=None,
          call_location_id='%s:%s' % (frame.f_code.co_filename,
                                      frame.f_lineno))