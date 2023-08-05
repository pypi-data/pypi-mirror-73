""" A Python interface for working with vallency lexicon data.




    The vallex module is a Python interface for working with vallency lexicon data.

    ===========================
    Example usage
    ===========================

    .. code-block:: python

        from vallex import LexiconCollection, add_file_to_collection
        from vallex.grep import parse_pattern, filter_db


        # Create a collection of lexicons
        coll = LexiconCollection()

        # Load a lexicon and add it to the collections
        add_file_to_collection(coll, open('v-vallex.txt', 'r', encoding='utf-8'))


        # Filter the collection looking for lexical units which have ACT in their frame
        pat = parse_pattern('frame.functor=ACT')
        coll = filter_db(coll, pat)


        # Print out the frame attribute of each lexical unit in the filtered
        # collection
        for lu in coll.lexical_units:
            print(lu.frame)
            
    ===========================
    Architecture
    ===========================
    
    The following is based on the article [VV2020]_.
    
    
    Data Layer
    ---------------------------
    A valency lexicon consists of a collection of *Lexemes*. A Lexeme represents a group of related
    lexical units that share the same lemma or (as in the case of Vallex, NomVallex, and other lexicons) 
    a group of derivationally related lemmas. Each lexical unit corresponds to a 
    single meaning of these lemmas. Each lexical unit can be annotated with a number 
    linguistic properties, e.g. semantic (a gloss of the given meaning, indication 
    of primary and metaphorical meanings), syntactic (does the given lexical unit 
    enter syntactic structures such as passive, reflexive and reciprocal 
    constructions?), and features specific to valency lexicons (the valency frame 
    and annotation of individual valency complementations with a functor, 
    obligatoriness and a list of possible forms of expressions; indication of 
    control, i.e. for a given lexical unit realizing one of its complementations 
    through an infinitive, indicate which other valency complementation is 
    referentially identical with the subject of this infinitive).

    The data layer definition is provided in the :mod:`vallex.data_structures` module
    and consists of the following classes:
    :class:`Lexicon <.data_structures.collections.Lexicon>` (representing a collection of *lexemes*),
    :class:`Lexeme <.data_structures.lexical_unit.Lexeme>` (representing a single *lexeme*), 
    :class:`LexicalUnit <.data_structures.lexical_unit.LexicalUnit>` (representing a *lexical unit*, i.e. a single meaning),
    :class:`Attrib <.data_structures.attribs.Attrib>` (representing a linguistically relevant property of a *lexical unit*). 
    The :class:`Attrib <.data_structures.attribs.Attrib>` class also has several specializations:
    :class:`Frame <.data_structures.attribs.Frame>` (representing the *valency frame*, represented as a list of *complementations*),
    :class:`Lemma <.data_structures.attribs.Lemma>` (representing the *lemma* or set of lemmas), and
    :class:`Specval <.data_structures.attribs.Specval>` (representing the changes between the valency of two related units,
    e.g. a verb and a deverbal noun or a verb and its translation to another language).
    It is expected that further specializations will be defined to deal with particular properties.

    Each of the above classes can store textual comments (which can be used to explain
    the reasoning behind a specific annotation, mark the data element as work in progress, etc)
    For efficiency reasons, they can also store the original unparsed form (in the original text-based format)
    together with its location in the source files, 
    and they all provide a method to convert the data into a JSON representable structure.

    Core components
    ---------------------------
    The core of the system consists of a *parser module* (:mod:`txt_parser <.txt_parser>`) which takes 
    care of parsing the data and constructing the data-layer---an in-memory representation of the data;
    a *search module* (:mod:`grep <.grep>`) which provides query capabilities; a *script module* 
    (:mod:`scripts <.scripts>`) which provides a framework for running data validation and batch processing scripts; 
    and an *output module* (currently implemented in :mod:`cli.common <.cli.common>`) which converts the in-memory representation into
    various output formats. Each of these components is implemented in a python submodule of the main :mod:`vallex <vallex>`
    module and the components are mostly independent of each other.

    
    The parser
    ^^^^^^^^^^
    The parse module (:mod:`txt_parser <.txt_parser>`) takes care of parsing the specialized format (see :ref:`fig:txt-fmt`) used by annotators when
    creating the lexicon data. The format is designed to be easily editable in any text editor and concise enough 
    to facilitate manual creation.
    
    .. code-block::
        :caption: Sample lexical unit in the textual format (simplified)
        :name: fig:txt-fmt

        : id: blu-v-brát-vzít-1
        ~ impf: brát (si) pf: vzít (si)
        + ACT(1;obl) PAT(4;obl) ORIG(od+2;opt)
            LOC(;typ) DIR1(;typ) RCMP(za+4;typ)
        -synon: impf: přijímat; získávat
                pf: přijmout; získat
        -example: impf: brát si od někoho mzdu
            pf: vzal si od něj peníze za práci
        -note: volné si
            mohli brát na odměnách.COMPL
                měsíčně 26 až 40 tisíc korun
        -recipr: ACT-ORIG
        -diat: no_poss_result no_recipient
            pf: deagent: peníze navíc se
                        musí odněkud vzít
                passive
            impf: deagent
            passive za práci se bere mzda

    The parser itself is split into a tokenizer function producing a stream of tokens and several
    parse methods. The methods take care of constructing the
    :class:`Lexeme <.data_structures.lexical_unit.Lexeme>`, 
    :class:`LexicalUnit <.data_structures.lexical_unit.LexicalUnit>`, and
    :class:`Attrib <.data_structures.attribs.Attrib>` classes. It is designed in such a way that 
    adding a specialized parser for a newly introduced property is just a matter of writing a single 
    function which is given the body of the attribute and returns an instance of (a descendant of) the 
    :class:`Attrib <.data_structures.attribs.Attrib>` class.
    To integrate the function into the parser, it is enough to decorate it with the provided
    Python decorator :meth:`AttributeFactory.register_parser <.txt_parser.AttributeFactory.register_parser>`.

    Search
    ^^^^^^
    The search module (:mod:`grep <.grep>`) provides query capabilities to the system.

    Queries
    '''''''
    A query is a collection of conditions
    and the result of the query is a set of lexical units each of which meets all
    of the conditions of the query [#disjunctive]_. Each condition consists of a *selector* 
    and a *pattern*.
    For each lexical unit the *selector* is passed to a ``match_key_values``
    function which constructs a list of strings. A lexical unit satisfies the condition if at
    least one of the strings matches the *pattern*, which is a regular expression.
    The *selector* is a dot-separated list of strings. The standard implementation of the
    ``match_key_values`` function (see :meth:`LexicalUnit.match_key_values <.data_structures.LexicalUnit.match_key_values>`) 
    interprets the first element of the selector as an attribute name which it retrieves. 
    It then passes the rest of the selector to the attribute's ``match_key_values`` function
    to construct the list of strings to be matched against. The standard implementation
    of the attribute's ``match_key_values`` method (see :meth:`Attrib.match_key_values <.data_structures.Attrib.match_key_values>`)
    returns the attribute's textual representation if the *selector* is empty, its source form
    if the selector is ``'src'`` and otherwise treats the selector as a path through the 
    attributes structure treated as a tree. It resolves the path and returns the value present
    in the relevant node. For example a query consisting of the single condition
    
    ::
    
        example.pf=.*od.*
        
    would match the lexical unit shown in :ref:`fig:txt-fmt` whose ``example`` attribute
    has the following structure
    ::
        {
            'impf': [ 'brát si od někoho mzdu'],
            'pf': ['vzal si od něj peníze za
                    práci']
        }
    
    The *selector* ``example.pf`` would retrieve the ``example`` attribute and from it
    its ``pf`` node which contains the string ``vzal si od něj peníze za práci``. This string
    incidentally matches the regular expression ``.*od.*``.

    For discoverability purposes, each attribute has a method (see :meth:`Attrib.match_keys <.data_structures.attribs.Attrib.match_keys>`) 
    which returns a lists of all valid paths inside its structure.
    
    Note that besides the internal structure of attributes output by the parser (Section :ref:`parser`),
    selectors may also access computed properties and results of tests (Section :ref:`sec:computed`);
    in particular, it is possible to formulate a query for all units that failed a given test,
    e.g. a query of the form
    ::
    
        error.lvc_references=.

    would match [#pattern]_ all lexical units that failed the test shown in Figure :ref:`fig:data-test-code`.
    
    ..  [#disjunctive] Experience seems to suggest that disjunctive conditions are not used very much. A limited spectrum of negative conditions can be formulated. At the cost of complexity of the query language, it would be easy to extend it to also additional types of queries.
    .. [#pattern] The pattern consists of a single dot so it matches any unit with a *non-empty* value of ``error.lvc_references`` .


    Executing queries
    '''''''''''''''''
    The search module (:mod:`grep <.grep>`) contains the :func:`grep <.grep.grep>` method to execute queries. 
    It additionally contains a :func:`filter <.grep.filter>` method which allows pruning each lexical unit in
    the result set so that it contains only the properties/attributes a user is interested in.
    
    The :func:`histogram <.grep.histogram>` method is provided to compute various histograms. It takes three 
    arguments: the first argument is a collection of lexical units over which the histogram is computed. 
    The second argument is a *selector* which produces a list of strings from each lexical unit in the same 
    way as is done when evaluating queries. The last argument is a regular expression which extracts the 
    values to be counted from each string from the list. :ref:`fig:histogram` shows how the UI displays the
    results of computing the histogram for the ``frame.functor`` selector with the trivial pattern (``.*``).
    
    .. figure:: ../_static/papers/2020_lrec/images/histogram.png
      :width: 300px
      :name: fig:histogram
      
      The web-based UI showing a histogram of the frame functors
    
    
    Scripts
    ^^^^^^^
    The script module (:mod:`scripts <.scripts>`) provides a framework for running simple procedures over the
    valency lexicon data. The scripts are loaded by the framework from a configurable directory. Each
    file in this directory is a Python source file containing the definitions of the procedures.
    The system currently recognizes five kinds of procedures: *test*, *transform*, *compute* and *map/reduce*.

    
    Test
    ''''
    The test procedures are used to implement data validation for the lexicon. Each test
    function receives a lexical unit as its argument [#test-subtypes]_. It checks whether the unit satisfies
    the test and raises an appropriate exception if it doesn't. The framework iterates over all lexical units 
    passing them in turn to each test procedure and collecting the results. The results are saved in the 
    in-memory representation and can then be displayed to the user (:ref:`fig:test-result`).
        
    .. figure:: ../_static/papers/2020_lrec/images/test-result.png
      :width: 300px
      :name: fig:test-result
      
      The web-based UI showing the result of a data-validation run on a lexical unit.
      
    The results are also annotated with the docstring of the test-procedure which can be used to provide human
    readable explanation of the failed result. An example data validation test is provided in :ref:`fig:data-test-code`.
    
    .. code-block:: python
      :name: fig:data-test-code
      :caption: An example of a data-validation procedure
    
        @requires('lumap')
        def test_lu_lvc_references(lu, lumap):
        \"""
            In attributes with links, each link
            should point to an existing lu.
        \"""
        failures = []
        lvc_variants = [k for k in lu.attribs.keys()
                            if k.startswith('lvc')]
        if not lvc_variants:
            raise TestDoesNotApply
        applies = False
        for attrib in lvc_variants:
            if not \
            isinstance(lu.attribs[attrib]._data,
                        dict):
            continue
            refs = lu.attribs[attrib]._data['ids']
            if refs:
            applies = True
            for ref in refs:
                if not ref._id.startswith('@') \
                and ref._id not in lumap:
                failures.append(str(ref._id))
        if failures:
            raise TestFailed("The following \
                    references not found in db: "
                    +','.join(failures))

    .. [#test-subtypes] Actually, there are four sub-types differing in what argument is passed --- a collection of lexicons, a single lexicon, a single lexeme or a lexical unit; for simplicity here and also in the paragraphs dedicated to other types of procedures we discuss only the sub-type receiving a lexical unit.
    

    Transform
    '''''''''
    The transform procedures can be used to implement one-time lexicon-wide changes, e.g.
    renaming an attribute. They receive a lexical unit which they can modify and return.

    
    Compute
    '''''''
    The compute procedures are similar to the transform procedures, but are used to implement 
    dynamically computed properties which are *not* saved back to the lexicon on disk.

    
    Map/Reduce
    ''''''''''
    The map/reduce procedures are used to perform more complicated analyses of the lexicon
    for which a simple search/histogram does not suffice. Each map/reduce procedure consists 
    of a pair of functions: a *mapper* and an (optional) *reducer*. Each mapper receives a
    lexical unit as an argument and uses a framework-provided ``emit`` function (see :func:`emit <.scripts.mapreduce.emit>`)
    to emit a collection of ``(key, value)`` pairs. The framework iterates over all lexical-units 
    passing them to the mapper functions and collecting the resulting pairs. It then groups them 
    by the ``key`` component and passes the groups to the reducer which can do further processing.
    A default reducer which just counts the number of values for a given key is provided by the 
    framework and is used when no specialized reducer is provided by the user. Note that, although 
    map/reduce is now commonly associated with parallel processing, here all the mappers and reducers 
    are run sequentially---while running them in parallel would be possible, the small size of the
    data does not justify the additional complexity of parallel processing. We use map/reduce only as 
    a familiar paradigm for structuring analysis code.


    Output
    ^^^^^^
    The output module provides tools to export lexicon data in various formats. In addition to built-in JSON
    output (which is implemented in the data-layer), new formats can be defined using 
    `Jinja2 <https://palletsprojects.com/p/jinja/>`_ templates.
    Currently only a single txt format is provided which outputs the in-memory representation in the same
    format that the annotators use. This can be used to check the fidelity of the in-memory representation
    (by comparing it with the original source) and for normalizing the sources. In the future other formats
    may be added, e.g., one of the XML-based internationally recognized formats such as `XML:TEI <https://tei-c.org/>`_
    or the RDF/XML serialization of the `OntoLex-Lemon <https://www.w3.org/2016/05/ontolex/>`_ model.

    The UI Layer
    ---------------------------

    Although the PyVallex system provides a command line UI for performing searches,
    computing histograms and running batch scripts, it is expected that most of its
    users will prefer a nicer graphical user interface. We have decided to provide
    the GUI as a web-based interface. This has several advantages. First, it allows 
    the system to be installed on a server and be accessible to users without forcing 
    them to acquire the needed datasets or requiring them to maintain the installation.
    Moreover, web-based technologies are very common and basing the UI on them 
    considerably lowers the barrier for new contributors/maintainers. It is expected 
    that even a person without a detailed knowledge of the system would be able to
    contribute simple modifications to the UI in a short amount of time. Finally, using 
    a webview widget provided by the `Qt library <https://qt.io>`_, we can implement
    a simple local client based on the same code-base.

    Implementation
    ^^^^^^^^^^^^^^
    The server-backend is a simple Python `WSGI <https://wsgi.readthedocs.io/en/latest/index.html>`_
    application written in the `Bottle.py <https://bottlepy.org/docs/dev/>`_
    microframework. It uses an `SQLite <https://www.sqlite.org/index.html>`_ database
    to store a JSON representation of the in-memory data [#database-concurrent]_
    and exposes a REST-based api which is consumed by the front end. The front end is 
    a Javascript application written using the `Vue.js framework <https://vuejs.org/>`_
    together with the `Vuetify 1.5 <https://v15.vuetifyjs.com/en/>`_ component library
    to provide a familiar `Polymer <https://www.polymer-project.org/>`_-style interface.
    
    .. [#database-concurrent] The database is used solely as a method to allow safe concurrent access to the data.

    ===========================
    Code Layout
    ===========================

    - The data structures for working with lexicon data are defined in the
      :mod:`vallex.data_structures` module. These are, mainly,

      * :class:`Lexeme <.data_structures.lexical_unit.Lexeme>`,
      * :class:`LexicalUnit <.data_structures.lexical_unit.LexicalUnit>`,
      * :class:`Attrib <.data_structures.attribs.Attrib>`

      plus a few other supporting classes.

    - Functions for parsing of the textual lexicon format are contained in the
      two :mod:`vallex.txt_parser` and :mod:`vallex.txt_tokenizer` modules.

    - Search/stats functionality is provided by the :mod:`vallex.grep` module

    - Infrastructure for the data validation tests is defined in the
      :mod:`vallex.tests` module

    - the command line client is contained in :mod:`vallex.cli`

    - the web based interface is contained in :mod:`vallex.server`, in particular
      the backend is in :mod:`vallex.server.app` and the frontend, written in
      Javascript and using the Vue & Vuetify frameworks is located in
      ``vallex/server/frontend``.
      
    .. [VV2020] Verner, J. and Vernerová A.: *PyVallex: A Processing System for Vallency Lexicon Data* (`pdf <../_static/papers/2020_lrec/main-submitted.pdf>`_), to appear in the proceedings of the `LREC 2020 <https://lrec2020.lrec-conf.org/en/>`_ conference.
"""
from pathlib import Path

from .config import Config, __appname__, __version__, __version_info__
from .utils import add_file_to_collection, add_path_to_collection, load_file, load_lexicon
from .data_structures import Lexicon, LexiconCollection, Lexeme, LexicalUnit, Frame, Lemma, Attrib, Specval
