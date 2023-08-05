""" This file contains definitions the Lexeme and LexicalUnit classes.





    This module contains two classes:

    - :class:`Lexeme` represents a lexeme
    - :class:`LexicalUnit` represents a lexical unit.

    which are used to represent the basic units of lexical data.
"""
import re

from typing import Dict, Iterable, List, Optional, Tuple

from ..json_utils import register as json_register
from ..location import Location

from .attribs import Attrib, Frame, Lemma
from .utils import Comment, AttrAccessor


@json_register
class Lexeme:
    """
        Represents a group of related lexical units.

        Attributes:
            comments:       A list of comments pertaining to the lexeme (i.e. those
                            in the txt-formatted source which occur before all the lexical units)
            lexical_units:  The list of lexical units belonging to the lexeme.
    """
    __slots__ = '_id', 'lexical_units', '_src_start', '_src_end', 'comments', '_errors'

    def __init__(self, lex_id: str):
        self._id = lex_id
        self.lexical_units: List[LexicalUnit] = []
        self.comments: List[Comment] = []
        self._src_start: Optional[Location] = None
        self._src_end: Optional[Location] = None
        self._errors: List[Tuple[str, str]] = []

    def __str__(self):
        return 'Lexeme(' + self._id + ')'

    def __json__(self, **opts):
        ret = {'id': self._id, 'lexical_units': self.lexical_units,
               'comments': self.comments, 'errors': self._errors}
        if self._src_start is not None:
            ret['source'] = self._src_start
        return ret

    def __len__(self):
        """
            Returns the number of lexical units in the lexeme.
        """
        return len(self.lexical_units)

    @classmethod
    def from_json(cls, dct):
        """
            Constructs a lexeme from a simple dict.
        """
        lex = Lexeme(dct['id'])
        lex.lexical_units = dct['lexical_units']
        lex._src_start = dct.get('source', None)
        lex.comments = dct.get('comments', [])
        for lu in lex.lexical_units:
            lu._parent = lex
        return lex


@json_register
class LexicalUnit(AttrAccessor):
    """
        Represents a group of related lexical units.

        Attributes:
            comments:   A list of comments pertaining to the lexeme (i.e. those
                        in the source which occur before all the lexical units)
            src:        The textual source of the lexical unit. Note that this might be empty, if the
                        source is not available (e.g. the lexical unit was loaded from json and its txt source
                        was not specified...)
            frame:      The frame attribute of the lexical unit
                        (see class:`Frame <vallex.data_structures.attribs.Frame>`)
            lemma:      The lemma attribute of the lexical unit
                        (see class:`Lemma <vallex.data_structures.attribs.Lemma>`)
    """

    __slots__ = '_id', 'attribs', 'dynamic_attrs', '_parent', '_src_start', '_src_end', '_src', 'comments', '_errors', 'frame', 'lemma'

    def __init__(self, lu_id: str, parent: Optional[Lexeme] = None):
        super().__init__(self, self.match_key_values, value_is_self=True)
        self._id = lu_id
        self.attribs: Dict[str, Attrib] = {}
        self.dynamic_attrs: Dict[str, Attrib] = {}
        self._parent = parent
        self.comments: List[Comment] = []
        self._src_start: Optional[Location] = None
        self._src_end: Optional[Location] = None
        self._src: Optional[str] = ''
        self._errors: List[Tuple[str, str]] = []  # TODO: generalize to "computed" properties
        self.frame = Frame()
        self.lemma = Lemma(data={})

    @property
    def src(self):
        """
            The source of the lexical unit in txt format.

            Note:   This might be empty, if the source is not available
                    (e.g. the lexical unit was loaded from json and its txt source
                    was not specified...)
        """
        if not self._src:
            if self._src_start is None or self._src_end is None:
                self._src = ''
            else:
                self._src = self._src_start._src[self._src_start.pos:self._src_end.pos]
        return self._src

    @property
    def all_comments(self) -> List[Comment]:
        """
            A list of all comments pertaining to the lexical unit.

            In the txt-formatted source, these are the comments occurring before any attribute is specified.
        """
        ret = self.comments
        if self.frame:
            ret += self.frame.all_comments
        if self.lemma:
            ret += self.lemma.all_comments
        for attrib in self.attribs.values():
            ret += attrib.all_comments
        return ret

    def __str__(self):
        return 'LexicalUnit(' + self._id+')'

    ATTR_EQUIVALENCE = {
        'example': ['example', 'examplerich', 'example1', 'example2', 'example3', 'example4', 'example5', 'example6', 'example7'],
        'lvc': ['lvc', 'lvc1', 'lvc2', 'lvc3', 'lvc4', 'lvc5', 'lvc6', 'lvc7', 'lvcN', 'lvcV'],
        'map': ['map', 'map1', 'map2', 'map3', 'map4', 'map5', 'map6', 'map7'],
        'instig': ['instig', 'instig1', 'instig2', 'instig3', 'instig4', 'instig5', 'instig6', 'instig7'],
        'recipr': ['recipr', 'recipr1', 'recipr2', 'recipr3'],
        'derived': ['derivedN', 'derivedV']
    }
    """
        A mapping of attributes which are considered equivalent when searching.

        The key is a general name for the group of attributes, the values are
        lists of attribute names in the group.
    """

    def match_keys(self) -> List[Tuple[str, str]]:
        """
            Returns a list of keys against which one can search (match).
        """
        ret = [
            ('id', 'id of the lexical unit'),
            ('src', 'source text of the lu'),
            ('error', 'list of validation error names'),
            ('comment', 'list of comments on the lu or any of its attributes'),
            ('lexicon', 'the source file the lu comes from')
        ]
        for attr in self.attribs.values():
            ret.extend(attr.match_keys())
        for dattr in self.dynamic_attrs.values():
            ret.extend(dattr.match_keys())
        if self.frame:
            ret.extend(self.frame.match_keys())
        if self.lemma:
            ret.extend(self.lemma.match_keys())
        return ret

    def match_key_values(self, key: Optional[List[str]] = None) -> Iterable[str]:
        """
            Returns a list of strings which are matched when when searching
            the `key` (see :module:`vallex.grep` for more information on
            how searching is implemented.)
        """
        if not key:
            return self.src

        # Special cases
        if key[0] == 'id':
            return [self._id]
        if key[0] == 'lexicon' and self._src_start:
            return [self._src_start._fname or '']
        if key[0] == 'src':
            return [self.src]
        if key[0] == 'frame' and self.frame:
            return self.frame.match_key_values(key[1:])
        if key[0] == 'lemma' and self.lemma:
            return self.lemma.match_key_values(key[1:])
        if key[0] == 'comment':
            return [str(c) for c in self.all_comments]
        if key[0] == 'error':
            if key[1:]:
                return sum([(test, msg) for test, msg in self._errors if key[1] in test], ())
            return sum([(test, msg) for test, msg in self._errors], ())

        match_against = self.ATTR_EQUIVALENCE.get(key[0], [key[0]]) + [
            attr.name for attr in self.attribs.values() if attr.duplicate == key[0]
        ]

        ret: List[str] = []
        for k in match_against:
            if k in self.attribs:
                ret.extend(self.attribs[k].match_key_values(key[1:]))
            elif k in self.dynamic_attrs:
                ret.extend(self.dynamic_attrs[k].match_key_values(key[1:]))

        return ret

    def __json__(self, **opts):
        ret = {'id': self._id, 'frame': self.frame, 'lemma': self.lemma,
               'attrs': self.attribs, 'comments': self.comments, 'errors': self._errors}
        if self._src_start is not None:
            ret['source'] = {
                'start': self._src_start,
                'end': self._src_end,
                'text': self.src
            }
        if opts.get('include_dynamic_attrs', False):
            ret['dynamic_attrs'] = self.dynamic_attrs
        return ret

    @classmethod
    def from_json(cls, dct):
        """
            Constructs a lexical unit from a simple dict.
        """
        lu = LexicalUnit(dct['id'])
        lu.frame = dct.get('frame', None)
        lu.lemma = dct.get('lemma', None)
        lu.attribs = dct['attrs']
        lu._src_start = dct.get('source', {'start': None})['start']
        lu._src_end = dct.get('source', {'end': None})['end']
        lu._src = dct.get('source', {'text': ''})['text']
        lu.comments = dct.get('comments', [])
        return lu
