import logging
import sys
import textwrap

from pathlib import Path

from vallex import error
from vallex.cli.common import load_lexicons, save_lexicons
from vallex.cli.lib import main_command, option, root, sub_command
from vallex.grep import parse_pattern, filter_db
from vallex.log import log
from vallex.scripts import load_script_file, run_script, run_scripts, RES_ERROR
from vallex.scripts.mapreduce import create_table, reduce
from vallex.term import FG, RED, GREEN, STATUS, YELLOW


@main_command()
def main(options={}):
    """Runs various scripts on the lexicons (data validation, stats computation, etc.)."""
    main.help()


@sub_command()
def test(options={}):
    """Runs data validation tests on the lexicons."""
    coll = load_lexicons(options)

    stats, failures = run_scripts(coll, 'test.')
    stats['parser'] = {k: 0 for k in error.ERROR_NAMES}

    for loc, error_tp, msg in error.DATA_ERRORS:
        if options['verbosity'] > 0:
            print(loc, ':', *msg)
        stats['parser'][error_tp] += 1

    def col(count):
        if count > 0:
            return FG(RED)
        return FG(GREEN)

    if options['verbosity'] > 0:
        for test_name, obj, message in failures:
            print(test_name, obj, message)

    total_errors = sum(stats['parser'].values())

    if total_errors > 0:
        print("Parser Errors:")
        for err_code, count in stats['parser'].items():
            print(" "*4, "{:<35}".format(error.ERROR_NAMES[err_code]+":"), col(count) | "{:>6}".format(count))
        print()

    for script_type, results in stats.items():
        if script_type == 'parser':
            continue
        print(script_type+" results:")
        for script_name, script_results in results.items():
            if script_results['error']:
                print(" "*4, "{:<35}".format(script_name+":"), FG(RED) | "{:>6}".format("TEST FAILED"), script_results['error'])
                total_errors += 1
            else:
                print(" "*4, "{:<35}".format(script_name+":"), col(script_results['fail']) | "{:>6}".format(script_results['fail']), "failed",
                      FG(GREEN) | "{:>6}".format(script_results['pass']), "passed",
                      FG(YELLOW) | "{:>6}".format(script_results['skip']), "skipped",
                      "(tot appl.:", str(script_results['pass']+script_results['fail'])+")")
                total_errors += script_results['fail']
        print()

    print()
    print("Total # of errors: {:>48}".format(FG(RED) | str(total_errors)))

    if total_errors > 0:
        return -1


@sub_command()
def transform(script_file, options={}):
    """Runs transform scripts on the loaded lexicons."""

    coll = load_lexicons(options)

    STATUS.start_action("Loading transform")
    transform_scripts = load_script_file(Path(script_file).absolute())
    STATUS.end_action()

    transformed_attrs = []
    for scr in transform_scripts:
        progress = STATUS.progress_bar("Running script "+scr.__name)
        res, msg = run_script(coll, scr)
        if res == RES_ERROR:
            progress.done(msg)
            log("cli", logging.ERROR, "Error running transform script", scr.__name, ":", msg)
            return -1
        else:
            progress.done()
        if hasattr(scr, '__transforms'):
            transformed_attrs.extend(scr.__transforms)

    save_lexicons(coll, options, transformed_attrs=transformed_attrs)


@sub_command()
def mapreduce(script_file, options={}):
    """Runs map-reduce scripts and prints the results as tab-separated tables."""
    coll = load_lexicons(options)

    STATUS.start_action("Loading mapreduce script")
    transform_scripts = load_script_file(Path(script_file).absolute())
    STATUS.end_action()

    progress = STATUS.progress_bar("Running mapper scripts")
    stats, _ = run_scripts(coll, 'mapreduce.map', progress_cb=progress.update)
    progress.done()

    failures = [(sn, stats['error']) for sn, stats in stats['mapreduce.map'].items() if 'error' in stats]
    if failures:
        progress.done('Failed')
        for script, msg in failures:
            STATUS.print("Script", script, "failed with message:\n", textwrap.indent(msg, "    "))
        return -1

    progress = STATUS.progress_bar("Running reducer scripts")
    results = reduce(progress_cb=progress.update)
    progress.done()

    out_file = options.get('output', None)
    if out_file:
        OUT = Path(out_file).open('w', encoding='utf-8')
    else:
        OUT = sys.stdout

    for table_name, res in sorted(results.items()):
        STATUS.print("="*70)
        STATUS.print(table_name.capitalize())
        STATUS.print("="*70)
        table, columns = create_table(res)
        key_len = len(next(iter(res.keys())))
        print(*['Key' + str(i+1) for i in range(key_len-1)], *[col.capitalize() for col in columns], sep='\t', file=OUT)
        for row in table:
            print(*row, sep='\t', file=OUT)
