""" mapreduce --- helper functions for map-reduce type scripts.




    This module provides the infrastructure to run map-reduce
    jobs on the lexicon. Each such job is defined by a pair
    of map-reduce functions.

    The map function should accept a lexical unit as its first
    parameter and produce (using the :func:`emit` function)
    a set of ``(key, value)`` pairs for it. The keys will typically
    be of type ``Tuple[str]`` and values can be anything (typically a number).

    The reduce function, if defined, should accept a ``key`` as its
    first parameter and a list of values as its second parameter and
    should produce a single value out of this list and return it.

    If a reduce function is not provided the ``sum`` function is used
    in its stead.

    Example: computing the total number of functors for nouns vs. verbs
    -------------------------------------------------------------------

    The following is a simple illustrative example. The reducer could
    have been omitted, since it uses just the default sum function.

    .. code::

        from vallex.scripts.mapreduce import emit

        def map_functor_count(lu):
            if lu.isNoun == ['True']:
                emit(('noun',), len(lu.frame.functor))
            elif lu.isVerb == ['True']:
                emit(('verb',), len(lu.frame.functor))

        def reduce_functor_count(key, resuts):
            return sum(results)


    Once saved to a file, say ``example-functor-counts.py`` one could
    use the ``vallex-cli`` to run it::

        $ vallex-cli mapreduce ./example-functor-counts.py

    which would produce the table::

        ========================================================
        Functor_count
        ========================================================
        noun    verb
         381      40

    (the numbers are made up for illustrative purposes)

    Note: currently all jobs are run serially (e.g. no multi-(threading|processing)
    is done).
"""
import logging
import sys

from collections import defaultdict
from typing import Any, Dict, Iterable, List, Optional, Tuple

from . import provides, SCRIPTS, RES_PASS
from ..log import log
from ..term import ProgressCallback

dd = defaultdict(lambda: defaultdict(list))  # type: ignore

MAP_RESULTS: Dict[str, Dict[Any, List]] = dd  # type: ignore
"The structure used to hold the values produced by different mappers"


def emit(key: Tuple, val):
    """
        Used by a mapper function to records the value ``val`` as a contribution
        to the key ``key``. The contribution is stored in the :attr:`MAP_RESULTS`
        structure under a key corresponding to the caller (the caller name minus
        the ``map_`` prefix).
    """
    caller_frame = sys._getframe().f_back
    caller_name = caller_frame.f_code.co_name  # type: ignore
    mapper_name = caller_name.lstrip('map_')
    MAP_RESULTS[mapper_name][key].append(val)


def reduce(progress_cb: Optional[ProgressCallback] = None):
    """
        Runs the corresponding loaded reducers to post-process results collected
        by the mappers. If a corresponding reducer is not found, a default one,
        which just sum the collected values for each key, is used.

        Optionally, if a `progress_cb` callback is provided, it is called with the
        fraction of the total number of reducers that have been run so far as first
        argument and the name of the currently running reducer as a second argument.
    """
    reduced_results: Dict[str, Dict[str, Any]] = defaultdict(dict)
    done = 0
    total = len(SCRIPTS['mapreduce.reduce'])
    mappers = set(MAP_RESULTS.keys())
    for script_name, script in [(sn, s) for sn, s in SCRIPTS['mapreduce.reduce'] if sn in mappers]:
        if progress_cb:
            progress_cb(done/total, script_name)
        for key, val in MAP_RESULTS[script_name].items():
            status, result = script(key, val)
            if status != RES_PASS:
                log("scripts:mapreduce", logging.ERROR, "Error reducing", script_name, "results:", result)
                break
            reduced_results[script_name][key] = result
        done += 1
        mappers.remove(script_name)
        if progress_cb:
            progress_cb(done/total, script_name)

    # For mappers without corresponding reducers
    # use a default reducer which just sums the
    # values
    for mapper_name in mappers:
        for key, val in MAP_RESULTS[mapper_name].items():
            try:
                reduced_results[mapper_name][key] = sum(val)
            except Exception as ex:
                log("scripts:mapreduce", logging.ERROR, "Error reducing", mapper_name, "results with default reducer:", ex)
                break
    return reduced_results


def create_table(results: Dict[Tuple, Any]) -> Tuple[List[List], List]:
    """
        Converts the reduced results `results` into a sorted
        table using the following procedure:

        Each ``(key, value)`` pair corresponds to a single cell whose
        coordinates ``(column, row)`` are ``(key[0], key[1:])``
        (i.e. row is the unique row which has ``key[1:]`` as the
        contents of the first ``len(key[1:])``-many cells).

        Returns:  A pair ``(table, columns)`` where ``table`` is the
                  lexicographically sorted table as a list of rows, each
                  row being a list of column values and ``columns`` is
                  a list of the generated column names (i.e. the
                  different ``key[0]`` values.)

        The function allows a single mapper to generate multiple
        results (columns) using the first element of the key as the
        column name, e.g.:

            emit('nouns', 'prod', 1)

        would contribute to the value of the column headed ``'noun'``
        in the row identified by ``'prod'``.
    """
    columns = sorted(list({key[0] for key in results}))
    rows = {key[1:] for key in results}
    table = []
    for row in rows:
        table.append(list(row)+[results[(col,)+row] if (col,)+row in results else None for col in columns])
    return sorted(table), columns
