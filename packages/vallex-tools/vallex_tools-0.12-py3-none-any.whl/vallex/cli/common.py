"""Utility functions used by cli commands.





   :func:`discover_formats` returns supported output formats
   :func:`load_lexicons`    loads lexicons based on commandline args & config
   :func:`saves_lexicons`   outputs lexicons to a destination and in a format specified by commandline args & config

"""
import logging
import re
import sys


from datetime import datetime
from pathlib import Path
from typing import Any, Dict, IO, List, Optional

from vallex import add_path_to_collection, error, LexiconCollection
from vallex.config import VALLEX_PACKAGE_PATH
from vallex.grep import filter_db
from vallex.json_utils import dump as json_dump
from vallex.log import log
from vallex.scripts import load_scripts, prepare_requirements, run_scripts
from vallex.term import STATUS


from .lib import root


try:
    import jinja2
    JINJA_ENV = jinja2.Environment(
        loader=jinja2.PackageLoader('vallex', 'templates'),
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True
    )
    HAVE_JINJA = True
except ImportError:
    HAVE_JINJA = False


def convert(collection: LexiconCollection, fmt: str, OUT: IO, transformed_attrs: Optional[List[str]] = None):
    """
        Saves the lexicon collection `collection` into the output stream `OUT`
        using format `fmt`. The `transformed_attrs` argument is passed to the
        template for its own use.
    """
    if fmt == 'json':
        json_dump(collection, OUT)
        return

    if not HAVE_JINJA:
        log("main:convert", logging.ERROR, "Jinja2 library, required for converting to", fmt, ", not present.")
        return

    try:
        tpl = JINJA_ENV.get_template(fmt+'.tpl')
        OUT.write(tpl.render({
            'collection': collection,
            'len': len,
            'str': str,
            'now': datetime.today(),
            'transformed_attrs': transformed_attrs
        }))
    except jinja2.TemplateNotFound as ex:
        log("main:convert", logging.ERROR, "Unable to find template", ex.name, "needed for outputting in", fmt, "format.")
    except jinja2.TemplateSyntaxError as ex:
        log("main:convert", logging.ERROR, "Template Syntax Error at", ex.filename+'('+str(ex.lineno)+'):', ex.message)
    except jinja2.TemplateError as ex:
        log("main:convert", logging.ERROR, "General Template Error:", ex.message)


def discover_formats() -> List[str]:
    """
        Returns a list of supported output formats.
    """
    ret = ['json']
    if HAVE_JINJA:
        package = VALLEX_PACKAGE_PATH / 'templates'
        for file_ in package.iterdir():
            if str(file_).endswith('.tpl'):
                ret.append(file_.name[:-4])
    return ret


def load_lexicons(options: Dict[str, Any]) -> LexiconCollection:
    """
        Loads the lexicons specified by the --load-lexicon/-i command line options
        or, if no such option is given, loads the lexicons from locations defined
        in the config file.
    """
    lexicon_sources = options.get('load-lexicon', []) or root.config.lexicons
    lexicon_coll = LexiconCollection()

    # Load the lexicons
    for lex_path in lexicon_sources:
        try:
            progress = STATUS.progress_bar("Loading "+Path(lex_path).name)
            add_path_to_collection(lexicon_coll, root.config, lex_path, progress_cb=progress.update)
            progress.done()
        except error.UnknownFormat as ex:
            progress.done()
            log("cli", logging.ERROR, str(ex))
        except FileNotFoundError:
            progress.done()
            log("cli", logging.ERROR, "Could not find", lex_path, "searched in", root.config.lexicon_dirs)

    STATUS.start_action("Loading scripts")
    load_scripts(root.config.script_dirs)
    STATUS.end_action()

    STATUS.start_action("Computing requirements")
    prepare_requirements(root.config, lexicon_coll)
    STATUS.end_action()

    progress = STATUS.progress_bar("Computing dynamic properties")
    run_scripts(lexicon_coll, 'compute', progress_cb=progress.update)
    progress.done()

    if options.get('pre-pattern', []) or not options['no-sort']:
        STATUS.start_action("Applying pre-patterns and/or sorting")
        lexicon_coll = filter_db(lexicon_coll, options.get('pre-pattern', []), no_sort=options['no-sort'])
        STATUS.end_action()

    return lexicon_coll


def save_lexicons(coll: LexiconCollection, options: Dict[str, Any], transformed_attrs: Optional[List[str]] = None):
    """
        Outputs the lexicon collection `coll` into the file specified by the --output/-o command line options
        or, if no such option is given, to standard output. The format is determined
        by the --output-format option.

        If `transformed_attrs` is provided, it is passed to the output template for its own use.

        If output is a directory, the output is split into several files in that directory, one for each
        lexicon in the collection.
    """
    fmt = options.get('output-format', None)
    outputs = None

    if 'output' in options:
        out_path = Path(options['output'])
        if out_path.is_dir():
            outputs = [(out_path / Path(p).name) for p in coll.lexicon_paths]
            OUT = None
        else:
            OUT = out_path.open('w', encoding='utf-8')
    else:
        OUT = sys.stdout

    if not fmt:
        if OUT and OUT.name.endswith('.json'):
            fmt = 'json'
        elif OUT and OUT.name.endswith('.db'):
            fmt = 'sql'
        else:
            fmt = 'txt'

    STATUS.start_action("Saving lexicons")
    if outputs:
        for out_path in outputs:
            lexicon = filter_db(coll, [(['lexicon'], re.compile(out_path.name))], no_sort=True)
            if lexicon.lexical_units:
                STATUS.update(out_path.name)
                with out_path.open('w', encoding='utf-8') as OUT:
                    convert(lexicon, fmt, OUT, transformed_attrs=transformed_attrs)
    elif OUT:
        convert(coll, fmt, OUT, transformed_attrs=transformed_attrs)
    STATUS.end_action()
