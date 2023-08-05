""" This module implements search related functionality.



    Searching in the lexicon is done by providing the :func:`filter_db`
    (or :func:`grep`) with a collection of lexemes and a pattern to
    searh for. The result is a list of lexemes which contain a matching
    lexical unit. The lexemes are modified so that the attribute
    :attr:`Lexeme.lexical_units <vallex.data_structures.lexical_unit.Lexeme.lexical_units>`
    contains only the matched lexical units.


    Patterns
    --------

    A pattern to search for is a list of conditions each of which must
    be satisfied for a lexical unit to match. Each condition is a
    ``(key, regexp)`` pair. The ``key``, which is a list of strings,
    determines what parts of the lexical unit to match against.
    It is provided to the :meth:`LexicalUnit.match_key_values
    <vallex.data_structures.lexical_unit.LexicalUnit.match_key_values>`
    method of each lexical unit which in turn returns a list of strings.
    The ``regexp`` is a compiled (using :func:`re.compile`) regular
    expression which is then tested on each string. If any string
    matches, the lexical unit is considered to match.

    This module also contains a utility function :func:`parse_pattern`
    to convert a string into a pattern. See the documentation of
    this function for the exact syntax the string needs to conform to.

    Determining Match Strings
    -------------------------

    As said above, the list of string against which the regular expression
    patterns are tested is determined by the :meth:`LexicalUnit.match_key_values
    <vallex.data_structures.lexical_unit.LexicalUnit.match_key_values>`
    method. This method is provided a key, which is a list of strings, e.g.::

        ['frame', 'functor']

    Typically, the first element of the list indicate which attribute to
    match against. The rest of the elements than specify what part of the
    attribute to match and are interpreted by the :meth:`Attrib.match_key_values
    <vallex.data_structures.attribs.Attrib.match_key_values>` method. In the
    above example, the result would be the list of functor names appearing in
    the frame attribute of the lemma. If the key contains just the first element,
    the resulting match string is typically the source text of the whole attribute
    as present in the lexicon source file.


    Attribute names
    ^^^^^^^^^^^^^^^

    Note that the attribute names do not correspond exactly to the attribute
    names present in the lexicon source data---several attributes are considered
    equivalent for the purpose of searching. For example if the first element
    of the ``key`` list is ``'lvc'``, the resulting list of strings to match
    against will be a union of the lists provided by each of the attributes
    ```lvc``, ``lvcN``, ``lvcV``, ``lvc1``..., so a lexical unit will match
    if any of these attributes match. The exact list of equivalent attributes
    is determined by the :attr:`LexicalUnit.ATTR_EQUIVALENCE
    <vallex.data_structures.lexical_unit.LexicalUnit.ATTR_EQUIVALENCE>` attribute.


    Computing Histograms
    --------------------

    This module also provides the function :func:`histogram` which can
    compute a histogram of attribute values in a lexeme collection.
    The values whose histogram is computed are determined in much the same
    way as the Match Strings (see above) using a key, which is a list of strings.
    One may also specify a regexp which selects only a part of each match string
    for the purpose of counting.

"""
import locale
import logging
import re
import sys

from collections import defaultdict
from contextlib import contextmanager
from functools import wraps
from typing import Dict, Iterable, List, Optional, Pattern, Tuple, Union

from .data_structures import Comment, LexiconCollection, Lexeme, Lexicon, LexicalUnit
from .json_utils import register as json_register
from .log import log


def parse_pattern(patterns: str) -> List[Tuple[List[str], Pattern]]:
    """ Converts a string describing a match condition into the format
        expected by :func:`grep`, :func:`filter_db` and :func:`histogram`.

        The parameter `patterns` is a ``&``-separated list of conditions,
        where each condition is of the form::

                KEY=REGEX

        where ``KEY`` is a dot-separated key, e.g.::

                example.impf

        or::

                synon

        and ``REGEX`` is a regular expression which is used for searching
        in the match strings.

        Returns:

            The function returns a list of pairs ``(key, pattern)`` where ``key`` is a list
            of strings and ``pattern`` is a compiled regular expression.
    """
    ret = []
    if patterns:
        pats = patterns.split('&')
        for pat in pats:
            key_str, pattern = pat.split('=')
            key = key_str.split('.')
            ret.append((key, re.compile(pattern, re.DOTALL)))
    return ret


def filter_attrs(lu: LexicalUnit, restrict_to_attrs: Optional[List[str]] = None) -> LexicalUnit:
    """
        If `restrict_to_attrs` is provided, creates a copy of the lexical unit `lu` with
        only the attriutes specified in `restrict_to_attrs`. Otherwise returns the original
        lexical unit.
    """
    if restrict_to_attrs is None:
        return lu
    new_lu = LexicalUnit(lu._id, lu._parent)
    if hasattr(lu, '_src_start'):
        new_lu._src_start = lu._src_start
        new_lu._src_end = lu._src_end
    if 'lemma' in restrict_to_attrs:
        new_lu.lemma = lu.lemma
    if 'frame' in restrict_to_attrs:
        new_lu.frame = lu.frame
    new_lu.attribs = {a: v for a, v in lu.attribs.items() if a in restrict_to_attrs}
    return new_lu


_WIN_LOCALE_MAP = {
    ('cs_CZ', 'UTF-8'): 'Czech'
}


@contextmanager
def _changedlocale(new_locale: Tuple[str, str]):
    """
        A context manager which changes the current active locale
        to the one specified by the pair `new_locale` and resets
        it back afterwards. This is useful mainly for locale-aware
        sorting.

        Example:

            with  _changedlocale(('cs_CZ','UTF-8')):
                print(sorted(['Štěpán', 'Stephen']))

    """
    if 'win' in sys.platform:
        new_locale = _WIN_LOCALE_MAP[tuple(new_locale)]  # type: ignore

    old_locale = locale.getlocale(locale.LC_COLLATE)
    try:
        locale.setlocale(locale.LC_COLLATE, new_locale)
        yield locale.strcoll
    except locale.Error as e:
        log("main:grep", logging.ERROR, 'Error setting locale to ', new_locale, ":", str(e))
        yield locale.strcoll
    finally:
        locale.setlocale(locale.LC_COLLATE, old_locale)


def _change_locale(loc: str):
    """
        A decorator which makes each call of the decorated function run
        with the active locale being `loc` (e.g. `cs_CZ.UTF-8`). This is
        useful mainly for locale-aware sorting.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with _changedlocale(loc.split('.')):
                return func(*args, **kwargs)
        return wrapper
    return decorator


def match_lu(lu: LexicalUnit, pattern: Pattern, key: Optional[List[str]] = None) -> bool:
    """
        Matches a compiled regular expression `pattern` against the lexical unit `lu`.
        The `key` parameter is used to specify what part of the lu to match against.
        If `key` is empty the match is performed against the source of the lu. Otherwise the
        first element should be an attribute name and the rest is an attribute path passed down
        to the :meth:`Attrib.match_key_values <vallex.data_structures.attribs.Attrib.match_key_values>`
        method of the attribute. If there is no attribute with the given name, False is returned.

        Returns:
            ``True`` if the lexical unit matches, ``False`` otherwise
    """

    values = lu.match_key_values(key or [])
    for val in values:
        if pattern.search(val):
            return True
    return False


def filter_db(db: LexiconCollection, patterns: Optional[List[Tuple[List[str], Pattern]]] = None, restrict_to_attrs: Optional[List[str]] = None, no_sort: bool = False) -> LexiconCollection:
    """
        A function to filter a collection of lexicons returning a new collection containing only the lexical units
        that match.

        Args:
            db:                 the collection of lexicons to filter
            patterns:           a list of (key, pattern) pairs specifying the match conditions
                                as required by :func:`grep`
            restrict_to_attrs:  if proviedd, the resulting lexical units will contain only the
                                specified attributes, other attributes will be discarded
            no_sort:            if false, the lexemes comprising the resulting collection will be sorted by
                                their :attr:`Lexeme._id <vallex.data_structures.lexical_unit.Lexeme._id>`
                                attribute.

    """
    ret = LexiconCollection()
    for lexicon in db.lexicons:
        ret.add_lexicon(Lexicon(grep(lexicon.lexemes, patterns, restrict_to_attrs=restrict_to_attrs,
                                     id_only=False, no_sort=no_sort)[0], lexicon._preamble, lexicon.path))
    return ret


@json_register
class Histogram:
    """A simple structure to hold a computed histogram """

    bins: Dict[str, int]
    """ The histogram bins, a mapping of values to the total number of their occurrences. """

    total: int
    """ The sum of the bins values """

    def __init__(self):
        self.bins: Dict[str, int] = defaultdict(int)
        self.total = 0

    def __json__(self, **opts):
        return {
            'bins': self.bins,
            'total': self.total,
        }


def histogram(db: LexiconCollection, key: List[str], select_regexp: Pattern) -> Tuple[Histogram, Histogram]:
    """
        Computes two histograms of attribute values of lexical units in the `db` collection.

        The values for which the histogram is computed are determined in a similar way as
        the matching strings which are used for searching (see above). In particular,
        for each lexical unit a list of matching strings is computed using the
        :meth:`LexicalUnit.match_key_values <vallex.data_structures.lexical_unit.LexicalUnit.match_key_values>`
        method which is passed the `key` as an argument. Next, each of these strings
        is matched against the `select_regexp` pattern. If the pattern does not match,
        the string is skipped. Otherwise there are two possible cases:

        1. `select_regexp` pattern does not contain any groups; in this case the value
           which will be counted is just the (currently first) part of the string
           that matches; or

        2. the `select_regexp` pattern contains at least one group; in this case each of
           the matched groups gives a value which is counted



        Args:
            db:             a lexicon collection which provides the lexical
                            units to compute the histogram over.
            key:            a list of strings which determines the matching strings
                            which contain the values which will be counted
            select_regexp:  a regexp which is used to extract the value to count out
                            of one of the matching strings

        Returns:
            The pair ``(occurrences, unique_lus)`` of computed histogram (instances of the
            `:class:Histogram` named tuple).
    """
    occurrences = Histogram()
    unique_lus = Histogram()

    for lu in db.lexical_units:
        values = lu.match_key_values(key)
        lu_selected_values = set()
        for match_string in values:
            m = select_regexp.search(match_string)

            if m:
                vals = [str(g) for g in m.groups()] if m.groups() else [str(m.group())]  # type: ignore
                for val in vals:
                    occurrences.bins[val] += 1

                lu_selected_values.update(vals)
                occurrences.total += len(vals)

        for val in lu_selected_values:
            unique_lus.bins[val] += 1
            unique_lus.total += 1
    return occurrences, unique_lus


@_change_locale('cs_CZ.UTF-8')
def grep(db: Iterable[Lexeme],
         patterns: Optional[List[Tuple[List[str], Pattern]]] = None,
         restrict_to_attrs: Optional[List[str]] = None,
         id_only=False,
         no_sort=False) -> Tuple[Union[Iterable[Lexeme], List[Tuple[str, str]]], Dict]:
    """
        A function which searches a collection of LexicalUnits for those matching a search pattern.

        Whether a lexical unit matches a pattern is determined using the :func:`match_lu` function.
        The exact procedure is described in its docs as well as in the module docs in more detail.


        Args:
            db:                 the list of lexemes whose lexical units will be searched
            patterns:           a list of search patterns each of which must match for lexical unit to
                                be included in the result
            restrict_to_attrs:  if present, the lexical units returned will only have attributes from
                                this list, all other attributes will be discarded
            id_only:            if true, a list of pairs ``(lex_id, lu_id)`` identifying each matched
                                lexical unit will be returned instead of the full lexical units
            no_sort:            if true, the results will not be sorted

        Returns:
            A tuple ``(results, stats)`` where ``results`` has the following interpretation:

            If `id_only` is ``False``, returns a list of Lexemes which each had at least one matching lexical unit. Each lexeme
            returned will have its :attr:`Lexeme.lexical_units <vallex.data_structures.lexical_unit.Lexeme.lexical_units>`
            attribute filtered so that it only contains those lexical units which matched each pattern
            in the provided list of patterns.

            Otherwise it returns a list of pairs ``(lex_id, lu_id)``, one for each matching lexical unit, where
            the first element is the id of the parent of the unit (i.e. the vaule of the
            :attr:`Lexeme._id <vallex.data_structures.lexical_unit.Lexeme._id>` attribute) and the second element is
            the id of the lu itself (i.e. the value of the :attr:`LexicalUnit._id <vallex.data_structures.lexical_unit.LexicalUnit._id>`
            attribute).

            The results are sorted according to the :attr:`Lexeme._id <vallex.data_structures.lexical_unit.Lexeme._id>`
            attribute of the lexemes unless `no_sort` is specified and ``True``, in which case no sorting is applied.

            While ``stats``, provided at least a single pattern is given, provides some statistics, computed according
            to the following rules:

            ``s celkem XXX jednotkami`` = celkový počet jednotek v lexémech, v nichž alespoň jedna jednotka matchuje (včetně jednotek, které dotazu neodpovídají); tento údaj možná není nutné uvádět

            ``což odpovídá YYY lemmatům`` = počet všech lemmat u matchujících jednotek, přičemž
                - opakující se lemma se počítá jen jednou
                - reflexivní a nereflexivní lemma je jiné lemma - tedy "dostávat1" a "dostávat1 se" jsou dvě lemmata, "brát", "brát si", "brát se" jsou tři
                - volné (se)/(si) se v počítání lemmat ignoruje, tj. počítá se to jako totožné s nereflexivním lemmatem, tj. "brát", "brát (si)", "brát si" jsou dvě, samotné "brát (si)" je jedno (!!!) lemma, "brát" a "brát (si)" je také jedno
                - varianty jsou samostatná lemmata, tj. "otvírat/otevírat" jsou dvě lemmata
                - homonyma se rozlišují, takže "dostávat1" a "dostávat2" jsou dvě lemmata
                - typ, že totéž lemma má uvedený různý vid (např. "pf: stát" a "impf: stát" nebo "pf1: stát" a "pf2: stát") by snad nikde nastat neměl (máme na to tuším nějaký test), ale pokud by se to stalo, současné vyhledávadlo by to nesprávně počítalo za jediné lemma, ač by se mělo jednat o lemmata dvě (a měla by být odlišena číselnou koncovkou na konci lemmatu jako homonyma)

            ``nerozlišujeme-li homonyma`` se počítá stejně jako výše, až na to, že "dostávat1" a "dostávat2" jsou totéž lemma, protože se ignorují číselné indexy u lemmatu (pozor u reflexiv - v současných datech teď je jen typ "lemma1 se" nebo "lemma1 si", ale v minulosti jsme měli i typ "lemma se1"); nejvyšší číselný index u homonym teď je 3, ale teoreticky by mohlo být i více)

            ``z toho neiterativních`` se počítá stejně jako výše, ale ignorují se všechna iterativní lemmata, tj. ta, před kterými je uvedeno "iter:", případně "iter1:" nebo "iter2:" (do vyšších čísel se snad zatím nedošlo, ale existuje "pf3", takže teoreticky asi je možné i "iter3")

            ``odpovídající počet lexikálních jednotek pro vidové protějšky zvlášť``: každá matchující lexikální jednotka se započítá tolikrát, kolik je v její hlavičce uvedeno lemmat (totéž ještě pro neiterativní)

    """
    if patterns is None:
        patterns = []
    if (not patterns) and (restrict_to_attrs is None) and (not id_only):
        log("main:grep", logging.DEBUG, 'Trivial filter matching all elements')
        if no_sort:
            return db, {}
        return sorted(db, key=lambda lex: locale.strxfrm(lex._id)), {}
    ret = []

    stats: Dict[str, int] = {
        'm_lexeme_count': 0,
        'm_lu_count': 0,
        'm_lexeme_lu_count': 0,
        'lemma_count': 0,
        'lemma_count_noiter': 0,
        'lemma_count_nodisc_hom': 0,
        'lemma_count_nodisc_hom_noiter': 0,
        'lu_cross_lemma_count': 0,
        'lu_cross_lemma_count_noiter': 0
    }
    lemma_set = set()
    lemma_set_noiter = set()
    lemma_set_nodisc_hom = set()
    lemma_set_nodisc_hom_noiter = set()

    enriched_patterns = [(path[:-1]+[path[-1].strip('!')], pat, path[-1].endswith('!')) for path, pat in patterns]

    for lex in db:
        # FIXME: Replace by a proper clone method on Lexeme
        new_lex = Lexeme(lex._id)
        new_lex.comments = [Comment(str(c)) for c in lex.comments]
        if hasattr(lex, '_src_start'):
            new_lex._src_start = lex._src_start
        for lu in lex.lexical_units:
            match = True
            for attrib_path, pattern, negated in enriched_patterns:
                m = match_lu(lu, pattern, attrib_path)
                if (negated and m) or (not negated and not m):
                    match = False
                    break
            if match:
                lemmas = lu.lemma.lemma_set()
                lemmas_noiter = lu.lemma.lemma_set(noiter=True)
                lemma_set.update(lemmas)
                lemma_set_noiter.update(lemmas_noiter)
                lemma_set_nodisc_hom.update(lu.lemma.lemma_set(discern_homo=False))
                lemma_set_nodisc_hom_noiter.update(lu.lemma.lemma_set(discern_homo=False, noiter=True))
                stats['lu_cross_lemma_count'] += len(lemmas)
                stats['lu_cross_lemma_count_noiter'] += len(lemmas_noiter)
                new_lex.lexical_units.append(filter_attrs(lu, restrict_to_attrs))
        if new_lex.lexical_units:
            stats['m_lexeme_count'] += 1
            stats['m_lexeme_lu_count'] += len(lex)
            stats['m_lu_count'] += len(new_lex)

            if id_only:
                ret.extend([(lu._id, new_lex._id) for lu in new_lex.lexical_units])
            else:
                ret.append(new_lex)  # type: ignore

    stats['lemma_count'] = len(lemma_set)
    stats['lemma_count_noiter'] = len(lemma_set_noiter)
    stats['lemma_count_nodisc_hom'] = len(lemma_set_nodisc_hom)
    stats['lemma_count_nodisc_hom_noiter'] = len(lemma_set_nodisc_hom_noiter)

    if id_only:
        if not no_sort:
            ret = sorted(ret, key=lambda pair: pair[1])
        return ret, stats  # type: ignore

    if not no_sort:
        ret = sorted(ret, key=lambda lex: locale.strxfrm(lex._id))  # type: ignore
    return ret, stats  # type: ignore
