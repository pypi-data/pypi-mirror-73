import textwrap

from vallex.cli.common import load_lexicons, save_lexicons
from vallex.cli.lib import main_command, option, root
from vallex.grep import parse_pattern, filter_db
from vallex.log import log
from vallex.term import FG, RED, GREEN, STATUS, YELLOW


@main_command()
def main(pattern='', options={}):
    """Search the lexicons.

       Expects a single argument --- the search pattern. Each search pattern
       is an '&'-separated list of conditions which are AND-ed together and
       each lexical unit is matched against the condition. In the end, only
       lexemes with matching lexical units are printed.

       Each condition is a key=pattern pair, where key is a match key and
       pattern is a regular expression. The condition is evaluated exactly
       as in the web frontend.
    """
    try:
        pattern = parse_pattern(pattern)
    except Exception as ex:
        STATUS.print(FG(RED) | "Invalid grep pattern", "'"+pattern+"'", "Error:", str(ex))
        return -1

    coll = load_lexicons(options)
    coll = filter_db(coll, pattern+options.get('post-pattern', []), no_sort=options['no-sort'])

    save_lexicons(coll, options)
