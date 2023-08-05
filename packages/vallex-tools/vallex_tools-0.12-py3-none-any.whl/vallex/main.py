#!/usr/bin/env python3
"""The vallex-cli command line interface





"""
import logging
import os
import sys

from pathlib import Path

from vallex import __version__   # type: ignore
from vallex.cli import lib as cli
from vallex.config import Config, _CONFIG_TEMPLATE, FROZEN, SCRIPT_DIR
from vallex.grep import parse_pattern
from vallex.log import root_logger, _CONSOLE_HANDLER, load_config
from vallex.term import STATUS


cli.load_commands('vallex.cli.commands')
cli.root.__doc__ = "A tool to work with Vallex data"
cli.root._version = __version__
cli.option("--load-lexicon", str, '-i', help="load a lexicon from this file", multiple=True)(cli.root)
cli.option("--output", str, '-o', help="file/dir to send output to")(cli.root)
cli.option("--output-format", str, help='output format')(cli.root)
cli.option('--pre-pattern',  str, help='A search pattern applied before operating on the loaded data', parser=parse_pattern)(cli.root)
cli.option('--post-pattern', str, help='A search pattern applied after operating on the loded data (before output)', parser=parse_pattern)(cli.root)
cli.option('--no-sort', bool, help='Do not sort the output')(cli.root)
cli.option("--verbosity", str, '-v',  help="Verbosity level (one of DEBUG, INFO, WARNING, ERROR, CRITICAL)", default='ERROR')(cli.root)
cli.option('--config', str, help='specify an alternate config file', default=os.environ.get('PY_VALLEX_CONFIG', 'pyvallex.ini'))(cli.root)


def main(argv):
    """
        The main entry point. Parses arguments, loads the config
        and delegates processing to the subcommands defined in the
        :module:`cli.commands` module.
    """
    cli.root.name = Path(os.getenv('_PY_VALLEX_PROGRAM_PATH', argv[0])).name

    try:
        # Parse the command line arguments & options
        cmd, args, opts = cli.root.parse(argv[1:], {})

        if not argv[1:]:
            # If there were no command line arguments
            # Use the gui command by default
            cmd = cli.root.get_command(['gui'])
            cmd.parse(argv[1:], opts)

        # Load configuration
        cli.root.config = Config(opts['config'])

        # Setup which log-level will be shown
        log_level = getattr(logging, opts['verbosity'].upper(), logging.ERROR)
        _CONSOLE_HANDLER.setLevel(log_level)
        load_config(cli.root.config)

        # If we are running the frozen executable
        # and there is no config file, create one
        # so that the user has a template which he can
        # modify
        if not cli.root.config.config_found() and FROZEN:
            (SCRIPT_DIR / cli.root.config._CFG_NAME).write_text(_CONFIG_TEMPLATE, encoding='utf-8')

        return cmd.main(*args, options=opts)
    except cli.CommandLineException as ex:
        STATUS.print(ex)
        STATUS.print()
        if ex._cmd:
            ex._cmd.help()
        else:
            cli.root.help()
        return -1


# Helper functions for package scripts (see the [tool.poetry.scripts] section
# of pyproject.toml)
def entry_point():
    return main(sys.argv) or 0


def gui_entry_point():
    return main([sys.argv[0], 'gui']+sys.argv[1:]) or 0


def web_entry_point():
    return main([sys.argv[0], 'web']+sys.argv[1:]) or 0


if __name__ == "__main__":
    sys.exit(main(sys.argv) or 0)
