import logging
import sys

from collections import defaultdict
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Union

from ..config import Config
from ..data_structures import Lexeme, LexicalUnit, Lexicon, LexiconCollection
from ..log import log, find_caller
from ..term import ProgressCallback
from ..utils import _import_python_file

from vallex.log import exc_formatter, _CONSOLE_HANDLER


Script = Callable[..., Tuple[int, Any]]
"The type of an arbitrary script for use in static typing."

_ScriptList = List[Tuple[str, Script]]
"A helper type for use in static typing."


_REQUIREMENTS: Dict[str, Dict[str, Any]] = {}
"""A dict holding the injectable arguments (a.k.a. requirements)"""


SCRIPTS: Dict[str, _ScriptList] = {}
"""A dict holding all the discovered scripts, keyed by script-type """

SCRIPT_TYPES = {
    'test_lu_': 'test.lu',
    'test_lexeme_': 'test.lexeme',
    'test_lexicon_': 'test.lexicon',
    'test_colection_': 'test.collection',
    'transform_lu_': 'transform.lu',
    'transform_lexeme_': 'transform.lexeme',
    'transform_lexicon_': 'transform.lexicon',
    'transform_colection_': 'transform.collection',
    'compute_': 'compute',
    'map_': 'mapreduce.map',
    'reduce_': 'mapreduce.reduce'
}
"""
    A dictionary mapping function prefixes to corresponding script types.
"""

DEFAULT_SEARCH_PATHS = [Path(__file__).parent/name for name in ['', 'tests', 'dynamic_properties']]
""" Default search paths for scripts. These are *always* searched. """


def prepare_requirements(config: Config, collection: LexiconCollection):
    """
        Computes injectable script arguments.
    """
    for req_name, req in _REQUIREMENTS.items():
        try:
            req['val'] = req['func'](config, collection)
        except Exception as ex:
            log("vallex.scripts", logging.ERROR, "Error computing script prerequisite", req_name, ":", ex)


def _objects_to_process(collection: LexiconCollection, script_type: str) -> Tuple[Iterable[Union[LexicalUnit, Lexeme, Lexicon, LexiconCollection]], int]:
    """
        Returns an iterable of objects to which the given `script_type` should be applied and the total number of objects
    """
    if script_type.endswith('lu'):
        return collection.lexical_units, len(collection)
    if script_type.endswith('lexeme'):
        return collection.lexemes, collection.lexeme_count()
    if script_type.endswith('lexicon'):
        return collection.lexicons, len(collection._lexicons)
    if script_type.endswith('collection'):
        return [collection], 1
    return collection.lexical_units, len(collection)


def run_scripts(collection: LexiconCollection, script_type: str, progress_cb: Optional[ProgressCallback] = None):
    """
        Runs all loaded scripts of type (starting with) `script_type` on the collection.

        Optionally, if a `progress_cb` callback is provided, it is called with the fraction of the
        total number of script runs that have been run so far as first argument and an empty message as
        second argument.
    """
    types = [st for st in SCRIPT_TYPES.values() if st in SCRIPTS and st.startswith(script_type)]
    stats: Dict[str, Dict[str, Dict[str, int]]] = {}
    stats = {t: defaultdict(lambda: defaultdict(lambda: 0)) for t in types}
    failures = []
    work_done = 0

    if progress_cb:
        total_work = sum([_objects_to_process(collection, t)[1]*len(SCRIPTS[t]) for t in types])

    for type_ in types:
        objects, _ = _objects_to_process(collection, type_)
        for script_name, script in SCRIPTS[type_]:
            if progress_cb and total_work > 0:
                progress_cb(work_done/total_work, script_name)
            for obj in objects:
                result, msg = script(obj)
                work_done += 1
                if result == RES_FAIL:
                    failures.append((script_name, obj, msg))
                    stats[type_][script_name]['fail'] += 1
                elif result == RES_PASS:
                    stats[type_][script_name]['pass'] += 1
                elif result == RES_SKIP:
                    stats[type_][script_name]['skip'] += 1
                elif result == RES_ERROR:
                    stats[type_][script_name]['error'] = msg
                    break
                if progress_cb and work_done % 100 == 0:
                    progress_cb(work_done/total_work, script_name)
    return stats, failures


def run_lu_scripts(lu: LexicalUnit, script_type: str) -> List[Tuple[str, str]]:
    """
        Runs all loaded scripts of type (starting with) `script_type` which operate on lexical units
        on the single lexical unit `lu`.

        Returns list of scripts which failed (or raised an unknown exception) together with appropriate
        error messages.
    """
    types = [st for st in SCRIPT_TYPES.values() if st in SCRIPTS and st.startswith(script_type)]
    failures: List[Tuple[str, str]] = []

    for type_ in types:
        for script_name, script in SCRIPTS[type_]:
            result, msg = script(lu)

            if result in (RES_FAIL, RES_ERROR):
                failures.append((script_name, msg))

    return failures


def run_script(collection: LexiconCollection, script: Script, progress_cb: Optional[ProgressCallback] = None):
    """
        Runs a single script given by `script` over the collection `collection`.

        Optionally, if a `progress_cb` callback is provided, it is called with the fraction of the
        total number of script runs that have been run so far as first argument and an empty message as
        second argument.
    """
    objects, total_work = _objects_to_process(collection, script.__type)  # type: ignore
    work_done = 0
    for obj in objects:
        result, msg = script(obj)
        if result == RES_ERROR:
            return RES_ERROR, msg
        work_done += 1
        if progress_cb and work_done % 100 == 0:
            progress_cb(work_done/total_work, script.__name)  # type: ignore
    return RES_PASS, ""


def load_script_file(path: Path) -> List[Callable]:
    """
        Loads scripts defined in the file pointed to by `path`.

        It tries importing the file and, if successful, finds all functions in the file
        which correspond to a supported script type (i.e. their name starts with one of the keys
        of :attr:`SCRIPT_TYPES <vallex.scripts.utils.SCRIPT_TYPES>`). These functions are
        then added to the :attr:`SCRIPTS <vallex.scripts.utils.SCRIPTS>` database under the
        respective script type key as a pair ``(script_name, function)``. If the script type
        is a test, the function is first wrapped using the :func:`wrap_test` decorator.
    """
    ret: List[Callable] = []
    try:
        mod = _import_python_file('vallex.scripts', path)
    except Exception as err:
        log('vallex.scripts', logging.ERROR, "Loading script", path, "failed with error", err)
        return ret
    for attr in dir(mod):
        for (prefix, script_type) in SCRIPT_TYPES.items():
            if attr.startswith(prefix):
                script = _wrap_script(getattr(mod, attr))
                script.__type = script_type
                script.__name = attr[len(prefix):]
                if script_type not in SCRIPTS:
                    SCRIPTS[script_type] = []
                SCRIPTS[script_type].append((script.__name, script))
                ret.append(script)
    return ret


def load_scripts(search_paths: Optional[List[str]] = None):
    """
        Loads extension scripts (e.g. data-validation tests, dynamic properties, transforms)
        from python files in `search_paths`.

        Searches the directories listed in `search_path` for all python files and loads the scripts
        they contain using the :func:`load_script_file` function.
    """

    search_dirs = DEFAULT_SEARCH_PATHS + ([Path(p) for p in search_paths or []])
    for sdir in search_dirs:
        for src in sdir.glob('*.py'):
            load_script_file(src)


RES_SKIP = 0
"The script does not apply to the given object"

RES_PASS = 1
"The script is a test, the test applies and passes"

RES_FAIL = 2
" The script is a test, the test applies and fails"

RES_ERROR = 3
""" There was an error running the script
    (the code resulted in an exception other than TestDoesNotApply or TestFailed)"""


def _wrap_script(script):
    """
        Wraps the function `script` into a function which first injects script requirements
        as keyword arguments and then calls the function in a try-except block
        catching *all* exceptions and returning a result code (see ``RES_*``
        constants) and the script return value. The TestDoesNotApply and TestFailed
        exceptions are handled specially via appropriate result codes.
    """
    @wraps(script)
    def wrapped(*args, **kwargs):
        if hasattr(script, '_requires'):
            reqs = {}
            for req in script._requires:
                if req not in _REQUIREMENTS or 'val' not in _REQUIREMENTS[req]:
                    return RES_ERROR, "Required argument '"+req+"' not provided."
                reqs[req] = _REQUIREMENTS[req]['val']
            kwargs.update(reqs)
        try:
            res = script(*args, **kwargs)
            return RES_PASS, res
        except TestDoesNotApply:
            return RES_SKIP, None
        except TestFailed as ex:
            return RES_FAIL, str(ex)
        except Exception as ex:
            if _CONSOLE_HANDLER.level == logging.DEBUG:
                return RES_ERROR, "".join(exc_formatter.format_exception(*sys.exc_info()))
            func_line = ex.__traceback__.tb_lineno
            error_msg = repr(ex)
            file_name, error_line, func_name, _ = find_caller(None)
            return RES_ERROR, error_msg+" in "+func_name+"("+file_name+":"+str(func_line)+"), line "+str(error_line)+""
    wrapped.__json__ = lambda **opts: {'name': wrapped.__name, 'doc': wrapped.__doc__}
    return wrapped


def changes(*attrs: str):
    """
        Returns a decorator which marks a script transform function as operating
        on the specified list `attrs` of lexical unit attributes.

    """

    def decorator(func):
        func.__transforms = attrs
        return func
    return decorator


def requires(*reqs: str):
    """
        Returns a decorator which marks a script function as requiring additional
        keyword arguments which will be injected when the script is run. The
        requirements must be provided by functions wrapped by a corresponding
        :func:`provides` decorator.

    """
    def decorator(func):
        func._requires = reqs
        return func
    return decorator


def provides(name: str):
    """
        Returns a decorator used to decorate functions which compute test prerequisites

        If a data-validation test needs some precomputation to be done (e.g. on the whole database),
        it can be decorated by the decorator returned from a :func:`requires`, e.g.::

            @requires('lexeme_count', 'lexical_unit_count')
            def test_lu_foo(lu, lexeme_count, lexical_unit_count):
              a = do_something_with(lu, lexeme_count)
              b = do_something_else(lu, lexical_unit_count)
              if (a and b):
                  raise TestFailed

        The test will then be passed additional arguments. These arguments will be computed
        once before any tests are run by functions decorated with a corresponding decorator
        provided by this method, e.g.::

            @provides('lexeme_count')
            def compute_dbsz(config, coll):
                return len(coll.lexemes)

            @provides('lexical_unit_count)
            def compute_lexical_unit_count(config, lexemes):
                return len(coll)

    """
    def decorator(func: Callable[[Config, LexiconCollection], Any]):
        _REQUIREMENTS[name] = {'func': func}
        return func
    return decorator


class TestDoesNotApply(Exception):
    """
        Exception that should be raised by data-validation tests
        when they are not applicable to the given object.
    """


class TestFailed(Exception):
    """
        Exception that should be raised by data-validation tests
        when the test fails
    """


@provides('lumap')
def construct_lumap(config: Config, coll: LexiconCollection):
    """Creates an id to lexical unit mapping for use in scripts. """
    ret = {}
    for lex in coll.lexemes:
        for lu in lex.lexical_units:
            ret[lu._id] = lu
    return ret


@provides('luidcount')
def construct_luidcount(config: Config, coll: LexiconCollection):
    """Creates an id to lexical unit mapping for use in scripts. """
    ret: Dict[str, int] = defaultdict(int)
    for lex in coll.lexemes:
        for lu in lex.lexical_units:
            ret[lu._id] += 1
    return ret


@provides('collection')
def collection(config: Config, coll: LexiconCollection):
    """Provides the collection object. """
    return coll
