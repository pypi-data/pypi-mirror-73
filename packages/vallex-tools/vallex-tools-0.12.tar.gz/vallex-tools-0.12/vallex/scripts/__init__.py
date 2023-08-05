""" This module provides infrastructure for running various scripts over source data.





    This module provides the infrastructure for running various scripts over source data as well as several
    example scripts.

    The infrastructure code is contained in :mod:`test.utils <vallex.test.utils>`. To use scripts, one needs
    to first call the :func:`load_scripts <vallex.scripts.utils.load_scripts>` function and then, before running
    any of the scripts, the :func:`prepare_requirements <vallex.scripts.utils.prepare_requirements>` function
    which expects a :class:`configparser.ConfigParser` instance as first argument and a
    :class:`LexiconCollection <vallex.data_structures.collections.LexiconCollection>' instance as a second argument.

    To run the scripts one would write code along the following lines::

        # Load a configuration file
        config = ConfigParser()
        config.read("config.ini")

        # Load the collection
        collection = load_file(...)

        # Precompute the requirements
        prepare_requirements(config, collection)

        # Run the ``test``-type scripts
        stats, failures = run_scripts(collection, "test")

    The loaded scripts are kept in the :attr:`SCRIPTS <vallex.scripts.utils.SCRIPTS` dictionary, keyed by script
    type with each value holding a list of pairs of the form ``(script_name, script_function)``.

    To run a single script, one uses the :func:`run_script <vallex.scripts.utils.run_script>` function, which
    needs a lexicon collection as its first argument and the script function as its second argument.

    (Both :func:`run_script <vallex.scripts.utils.run_script>` and :func:`run_scripts <vallex.scripts.utils.run_scripts`
    accept an optional `progress_cb` argument for reporting on the progress made.)

    Scripts are written as functions in python files in the directories specified
    by the ``script_dirs`` key in the config file. Some scripts are also provided
    in the :mod:`vallex.scripts.tests` and :mod:`vallex.scripts.dynamic_properties`
    package. However, these packages should not be imported, they are automatically loaded
    when calling load_scripts.  The names of the files do not matter
    (load_scripts inspects every python file in the searched directories)
    and can be used for grouping related scripts (e.g. the file ``verb_tests.py`` contains
    scripts performing data-validation tests pertaining to verbs). Each script needs to be a function
    whose name starts with one of the prefixes listed in :attr:`SCRIPT_TYPES <vallex.scripts.utils.SCRIPT_TYPES>`
    map. The prefix determines:

        1. what type of script it is (e.g. a data-validation test, a transform script or a script computing dynamic attributes)
        2. what is the object on which it operates (i.e. a lexical collection, lexicon, lexeme or a lexical unit)


    The function must accept as its first argument the respective object on which it operates. In case it is a
    data-validation test it should:

    - raise a :class:`TestDoesNotApply <vallex.scripts.utils.TestDoesNotApply>` error in case the test is not applicable
    - raise a :class:`TestFailed <vallex.scripts.utils.TestFailed>` exception in case the test failed

    If the script runs successfully without raising any exceptions, its return value, which should
    be a string, will be passed as a message from the script (e.g. from the :func:`run_script <vallex.scripts.utils.run_script>` function)
    and should be user-readable, i.e. suitable for printing to the console.

    Any exception raised inside the script function are caught by the runner (actually by a wrapper function)
    and a corresponding result (i.e. :attr:`RES_SKIP <vallex.scripts.utils.RES_SKIP>`, :attr:`RES_FAIL <vallex.scripts.utils.RES_FAIL>` or
    :attr:`RES_ERROR <vallex.scripts.utils.RES_ERROR>`) is returned from the script (or added to the stats in case of
    the :func:`run_script <vallex.scripts.utils.run_scripts>` function) together with the message provided in the exception.

    The first two codes (:attr:`RES_SKIP <vallex.scripts.utils.RES_SKIP>`, :attr:`RES_FAIL <vallex.scripts.utils.RES_FAIL>`) are useful
    mainly for data-validation tests and are set when the respective :class:`TestDoesNotApply <vallex.scripts.utils.TestDoesNotApply>`
    and :class:`TestFailed <vallex.scripts.utils.TestFailed>` are raised. The last code is for any other exception and, if the
    function finishes without raising an exception, the appropriate code is :attr:`RES_PASS <vallex.scripts.utils.RES_PASS>`.

    Each script function should also have docstring describing its use.

    If a script needs some precomputation to be done (e.g. on the whole database),
    it can be preceded by a ``@requires('req1', 'req2', ...)`` decorator and a corresponding
    function providing the results of the precomputation should be defined and
    decorated with the ``@provides('req1')`` decorator. For example::

        @provides('id_to_lu_map'):
        def construct_id2lu(collection):
            ret = {}
            for lu in collection.lexical_units:
                ret[lu._id] = lu
            return ret

        @provides('number_of_lexemes):
        def num_lex(colection):
            return len(collection.lexemes)

        @requires('id_to_lu_map', 'number_of_lexemes'):
        def test_lu_foo(collection, id_to_lu_map, number_of_lexemes):
            if number_of_lexemes < 100:
            raise TestDoesNotApply("Test only applies to large databases :-)")
            for ref in lu.attribs['lvc']['ids']:
                if ref._id not in id_to_lu_map:
                    raise TestFailed("Unknown reference: "+ref._id)
"""

from .utils import Script, RES_ERROR, RES_FAIL, RES_PASS, RES_SKIP
from .utils import changes, provides, requires, TestDoesNotApply, TestFailed
from .utils import load_script_file, load_scripts, prepare_requirements, run_lu_scripts, run_script, run_scripts, SCRIPT_TYPES, SCRIPTS
