from vallex.cli.lib import main_command, option, root, sub_command
from vallex.config import FROZEN, SCRIPT_DIR, VALLEX_PACKAGE_PATH
from vallex.scripts import SCRIPTS, load_scripts
from vallex.term import FG, RED, GREEN, YELLOW

from vallex.cli import common


@main_command()
def main(options={}):
    """Show various environment settings."""
    print("Frozen:", FROZEN)
    print("Package dir:", VALLEX_PACKAGE_PATH)
    print("Script dir:", SCRIPT_DIR)
    print("Config search paths:", [str(p) for p in root.config.config_paths])
    print()
    main.help()


@sub_command()
def formats(options={}):
    """Show available output formats."""
    for fmt in common.discover_formats():
        print(fmt)


@sub_command()
def scripts(script_type='', options={}):
    """Show available scripts."""
    load_scripts(root.config.script_dirs)
    for script_type, script_list in SCRIPTS.items():
        if script_type.startswith(script_type):
            print(script_type+":")
            print("  "+"\n  ".join([script_name for script_name, script in script_list]))


@sub_command()
def config(options={}):
    """Shows the configuration."""
    print(root.config)


@sub_command()
def lexicons(options={}):
    """Shows available lexicons."""
    print("Vallex repo version", root.config.get_repo_version())
    for lexicon in root.config.lexicons:
        print(lexicon.name)
