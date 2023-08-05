import re

from vallex.cli.common import load_lexicons
from vallex.cli.lib import main_command, option
from vallex.grep import histogram
from vallex.term import get_terminal_size, FG, RED, GREEN, Interpolator


@option('--value-selector',  str, help='A regexp to select the histogram value to count', default='.*')
@main_command()
def main(match_key, options={}):
    """Compute a histogram of the values of the provided match key."""

    coll = load_lexicons(options)

    occurrences, unique_lus = histogram(coll, match_key.split('.'), re.compile(options['value-selector']))
    hist, total = occurrences.bins, occurrences.total
    if not hist:
        print(FG(RED) | "No values found")
        return -1

    max_val_len = max([len(k) for k in hist.keys()])
    max_count = max(hist.values())
    term_width, _ = get_terminal_size()
    bar_len = min(term_width - max_val_len, 90)
    max_star_count = int((max_count/total)*bar_len)
    interp = Interpolator(1, (255, 255, 0), GREEN)
    for val, count in sorted(hist.items(), key=lambda x: x[1]):
        COL = FG(interp.col(count/total))
        first_sep = ' '*(max_val_len-len(val))
        star_count = int((count/total)*bar_len)
        second_sep = (max_star_count-star_count)*' '
        print(COL | val+first_sep, COL | star_count*'*'+second_sep, '('+str(count)+'/'+str(total)+')')
