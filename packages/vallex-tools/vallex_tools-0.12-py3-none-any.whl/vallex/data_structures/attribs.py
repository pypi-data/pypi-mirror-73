""" This file contains classes used to represent lexical unit attributes




    List of classes
    ---------------

    - :class:`Attrib` the base class of all attributes
    - :class:`Lemma`  represents the (mandatory) lemma attribute
    - :class:`Frame`  represents the (mandatory) frame attribute
    - :class:`FrameElement` a helper class representing the parts (functors) of the frame attribute
    - :class:`Specval`  represents a diff between the frame of a noun and the frame of a verb it's derived from
    - :class:`SpecvalElement` a helper class representing the parts (functors) of the specval attribute
"""
import re

from typing import Any, Dict, Iterable, List, Optional, Tuple, Set

from ..json_utils import register as json_register
from ..location import Location
from .utils import Comment, AttrAccessor
from .constants import ACTANT_FUNCTORS, ACTANTS_AND_CPHR


@json_register
class Attrib(AttrAccessor):
    """
        The base class of all lexical unit attributes.

        Attributes:
            name:        the name of the attribute
            _data[str]:  the value of the attribute as specified in the source
                         excluding comments
            comments:    the comments pertaining to the attribute
            _dynamic:    whether the attribute is computed or stored in the data
            _help:       the help text to show for the attribute search key
    """
    __slots__ = 'name', '_data', 'comments', '_src_start', '_src_end', 'duplicate', '_dynamic', '_help'

    def __init__(self, attr_name: str, data: Optional[Any] = None, help: str = '', dynamic: bool = False):
        super().__init__(self, self.match_key_values, value_is_self=True)
        self.name = attr_name
        self.comments: Dict[str, List[Comment]] = {'all': []}
        self._data: Any = data
        self._src_start: Optional[Location] = None
        self._src_end: Optional[Location] = None
        self.duplicate: str = ''
        self._dynamic = dynamic
        self._help = help

    @property
    def src(self):
        """
            The source of the attribute in txt format.

            Note:   If the source is not available (e.g. the lexical unit was loaded from
                    json and its txt source was not specified...) a best-effort is made
                    to produce a source in txt format, though no guarantees
                    on the correctness are provided.
        """
        if self._src_start is None or self._src_end is None:
            ret = '    -'+self.name+': '+str(self)
            comments = sum(self.comments.values(), [])
            if comments:
                ret += '#'+'\n            #'.join([str(c) for c in self.comments.values()])
            return ret
        ret = self._src_start._src[self._src_start.pos:self._src_end.pos]  # type: ignore
        if '\n' in ret:
            return ret[:ret.rindex('\n')]
        else:
            return ret

    @property
    def all_comments(self) -> List[Comment]:
        """
            A list of all comments pertaining to this attribute (i.e. all the
            comments which, in the txt-formatted source, appear before the next
            attribute/lexical unit/lexeme)
        """
        return sum(self.comments.values(), [])

    @classmethod
    def _resolve(cls, tree: Any, path: List[str]) -> list:
        """
            Returns the nodes with path `path` from the tree `tree` or ``None``
            if no such nodes exists. The `tree` argument can either be a ``dict``,
            in which case its children are its values and the edges are labeled by
            the keys or it may be an object, in which case its children are the
            objects attribute values and the edges are labeled by the attribute names.
            If a node is a list, it is replaced with its children and the path traversal
            is done for each child. Anything else is considered to be a tree with a
            single node --- the root, which is `tree` itself.
        """
        if not path:
            return tree
        if isinstance(tree, list):
            return sum([cls._resolve(ch, path) for ch in tree], [])
        if isinstance(tree, dict):
            child = tree.get(path[0], None)
        elif hasattr(tree, path[0]):
            child = getattr(tree, path[0])
        else:
            child = None

        if child is None:
            return []
        return cls._resolve(child, path[1:])

    @classmethod
    def _get_values(cls, obj: Any) -> List[str]:
        """
            Consider's obj to be a tree (in the same sense as in :meth:`Attrib._resolve`) and
            returns all its leaf values stringified.
        """
        if isinstance(obj, list):
            return sum([cls._get_values(elt) for elt in obj], [])
        if isinstance(obj, dict):
            return sum([cls._get_values(elt) for elt in obj.values()], [])
        if obj is None:
            return []
        return [str(obj)]

    @classmethod
    def _get_paths(cls, obj: Any) -> List[List[str]]:
        """
            Returns all paths through the tree obj.
        """
        if isinstance(obj, list):
            return sum([cls._get_paths(ch) for ch in obj], [])
        if isinstance(obj, dict):
            ret = []
            for key, val in obj.items():
                ret.append([key])
                ret.extend([[key]+sub_path for sub_path in cls._get_paths(val)])
            return ret
        return [[]]

    def match_key_values(self, key) -> Iterable[str]:
        """
            Returns a list of strings which are matched when when searching
            the `key` (see :module:`vallex.grep` for more information on
            how searching is implemented.)
        """
        if key and key[0] == 'src':
            # Return the source without the attribute name itself
            return [self.src.strip()[len(self.name)+2:].strip()]

        if key and key[0] == 'comment':
            if key[1:]:
                return [str(comment) for comment in self.comments.get(key[1], [])]
            return [str(comment) for comment in self.all_comments]

        objs = self._resolve(self._data, key)

        return self._get_values(objs)

    def match_keys(self) -> List[Tuple[str, str]]:
        """
            Returns a list of valid match_keys against which a search may be
            performed (see :module:`vallex.grep` for more information on
            how searching is implemented.). The keys are returned as pairs
            ``(key, desc)``, where ``key`` is the actual match key and ``doc``
            is a human readable description of the key.

            For the base class general implementation, each match_key is a dot-separated
            string. E.g. for the 'example' attrib._data may be::

                {
                    'all': ['A', 'whatever', '...'],
                    'impf': [],
                    'pf':['skonal']
                }

            in which case match_keys() would return::

                [
                    ('example', 'all examples'),
                    ('example.all', 'examples common to all aspects'),
                    ('example.'pf', 'examples of the pf aspect')
                ]

            Note, however, that the general implementation will actually return empty
            descriptions since it has no way to know them.

        """
        prefix = self.duplicate or self.name
        ret = [
            (prefix, self._help),
            (prefix+'.src', 'source text of ' + prefix),
            (prefix+'.comment', 'comments on ' + prefix)
        ] + [
            (prefix+'.comment.'+k, 'comments on the '+k+' part of '+prefix) for k in self.comments.keys()
        ]

        ret.extend([(prefix+'.'+('.'.join(path)), '') for path in self._get_paths(self._data)])

        return ret

    def __str__(self):
        return str(self._data)

    def __json__(self, **opts):
        return {'name': self.name, 'data': self._data, 'comments': self.comments, 'duplicate': self.duplicate}

    @classmethod
    def from_json(cls, dct):
        """
            Constructs an attribute from a simple dict.
        """
        attr = cls(dct['name'])
        attr._data = dct['data']
        attr.duplicate = dct['duplicate']
        attr.comments = dct['comments']
        return attr


@json_register
class Lemma(Attrib):
    """
        A class representing the lemma attribute of a lexical unit.

        The lemma attribute (indicated by ~ in the txt-formatted source)
        is a list of the forms of the lexical unit in various aspects.
    """
    _data: Dict[str, str] = {}

    def __init__(self, attr_name: str = '~', data: Optional[Any] = None):
        super().__init__(attr_name, data)

    def match_keys(self):
        """
            Searching may either be done on the whole lemma (``lemma``), on the
            aspects present (``lemma.aspect``) or on the form of a particular
            aspect (e.g. ``lemma.impf``).

            For more details on search see :module:`vallex.grep`.
        """
        return [
            ('lemma', 'forms of the lu (all aspects)'),
            ('lemma.aspect', 'aspects present in the lemma')
        ] + [('lemma'+'.'+k, 'lu form (in '+k+' aspect)') for k in self._data.keys()]

    def match_key_values(self, key: List[str]) -> Iterable[str]:
        """
            Returns a list of values against which to perform a search given the `key`.
        """
        if key:
            if key[0] == 'aspect':
                return self._data.keys()
            if key[0] in self._data:
                return [self._data[key[0]]]
            return []
        return self._data.values()

    def lemma_set(self, discern_homo: bool = True, noiter: bool = False) -> Set[str]:
        """
            Returns the set of lemmas. If `discern_homo` is ``False``, all numbers
            are stripped from the lemmas (corresponding to the fact that, e.g. ``dostávat1``
            and ``dostávat2`` are homonymous), If ``noiter`` is ``True`` the set
            will not contain lemmas corresponding to the ``iter`` aspect.

            Lemmas with a free (se)/(si) are considered equal to those without.
        """
        ret = set()
        for (aspect, lemma) in self._data.items():
            if not noiter or not aspect.startswith('iter'):
                if not discern_homo:
                    lemma = re.sub('[0-9]', '', lemma)
                lemma = re.sub(r'\([sei][sei]\)', '', lemma)
                lemmas = [l.strip() for l in lemma.split('/')]
                ret.update(lemmas)
        return ret


@json_register
class FrameElement:
    """
        A class representing a single element of the ``Frame`` attribute, e.g.::

            ORIG(od+2;opt)

        Attributes:

            functor:   the functor (e.g. ``ORIG``)
            forms:     a list of forms, each form being an (optional) preposition + case (e.g. ``od+2``)
            oblig:     the obligatory type (e.g. ``opt``, ``obl``, ...)
    """
    __slots__ = 'functor', 'forms', 'oblig'

    def __init__(self, functor: str, forms: Optional[List[str]] = None, oblig: Optional[str] = None):
        self.functor: str = functor
        self.forms = forms or []
        self.oblig = oblig

    def __str__(self):
        args = []
        if self.forms:
            args.append(','.join(self.forms))
        if self.oblig:
            args.append(self.oblig)
        if args:
            args = '('+';'.join(args)+')'
        else:
            args = ''
        return self.functor+args

    def match_key_values(self, key: List[str]) -> Iterable[str]:
        """
            Returns a list of strings which are matched when when searching the `key`
            (where `key` is either empty --- match against the full element, or
            ``oblig``, ``functor`` or ``forms`` in which case the matching is performed
            against the respective attribute)

            For more details on search see :module:`vallex.grep`.
        """
        if not key:
            return [str(self)]
        if key[0] == 'oblig' and self.oblig is not None:
            return [self.oblig]
        if key[0] == 'functor':
            return [self.functor]
        if key[0] == 'form':
            return self.forms
        if key[0] == 'forms':
            return [','.join(self.forms)]
        if key[0] == 'functor:form':
            return [self.functor+':'+form for form in self.forms]
        return []

    def __eq__(self, other):
        if not isinstance(other, FrameElement):
            return False
        return self.functor == other.functor and set(self.forms) == set(other.forms) and self.oblig == other.oblig

    def __json__(self, **opts):
        return {'functor': self.functor, 'forms': self.forms, 'oblig': self.oblig}

    @classmethod
    def from_json(cls, dct):
        """
            Constructs a frame element from a simple dict.
        """
        return FrameElement(dct['functor'], dct['forms'], dct['oblig'])


@json_register
class Frame(Attrib):
    """
        A class representing the ``Frame`` attribute of a lexical unit.

        The frame attribute (indicated by + in the txt-formatted source)
        is a list of elements, where each element specifies a functor and, optionally,
        a list of forms and the obligatory type, e.g.::

            + ACT(1;obl) PAT(4;obl) ORIG(od+2;opt) LOC(;typ) DIR1(;typ) RCMP(za+4;typ)

        Attributes:

            _data:  The list of frame elements
    """
    _data: List[FrameElement] = []

    def __init__(self, attr_name: str = '+', data: Optional[List[FrameElement]] = None):
        super().__init__(attr_name, data or [])

    def match_keys(self):
        """
            Searching may either be done on the whole fram (``frame``), on the
            list of functors (``frame.functor``), on the forms (``frame.forms``),
            on the obligatory types (``frame.oblig``) the txt-formatted source
            of the whole attribute (``frame.src``) or the comments (``frame.comments``).

            For more details on search see :module:`vallex.grep`.
        """
        ret = [
            ('frame', 'list of slot sources'),
            ('frame.src', 'source text of the frame'),
            ('frame.comments', 'comments on the frame'),
            ('frame.functor', 'list of functors'),
            ('frame.form', 'list of all forms (in all functors)'),
            ('frame.forms', 'list of all form-tuples (one per functor)'),
            ('frame.actant', 'list of all ACTANT functors'),
            ('frame.actant.form', 'list of all forms (in all ACTANT functors)'),
            ('frame.actant.forms', 'list of all form-tuples (one per each ACTANT functor)'),
            ('frame.oblig', 'list of obligatory types'),
            ('frame.functor:form', 'list of functor;form pairs (one per each form of each functor)'),
            ('frame.actant:form', 'list of functor;form pairs (one per each form of each actant functor)'),
        ]
        ret.extend([
            ('frame.'+slot.functor, 'source of the '+slot.functor+' slot') for slot in self._data
        ])
        ret.extend([
            ('frame.'+slot.functor+'.forms', 'the forms of '+slot.functor+' slot') for slot in self._data
        ])
        ret.extend([
            ('frame.'+slot.functor+'.oblig', 'the obligatory type of'+slot.functor+' slot') for slot in self._data
        ])
        return ret

    def match_key_values(self, key: List[str]) -> Iterable[str]:
        """
            Returns a list of strings which are matched when when searching the `key`
            (for the list of available keys see :meth:`Frame.match_keys`).

            For more details on search see :module:`vallex.grep`.
        """
        if not key:
            return [str(el) for el in self.elements]
        if key[0] == 'src':
            return [str(self)]
        if key[0] == 'comments':
            return sum([c.match_key_values([]) for c in self.all_comments], [])
        if key[0] in ['functor', 'form', 'forms', 'oblig', 'functor:form']:
            return sum([elt.match_key_values(key) for elt in self._data], [])
        if key[0] == 'actant':
            if key[1:]:
                return sum([elt.match_key_values(key[1:]) for elt in self._data if elt.functor in ACTANT_FUNCTORS], [])
            else:
                return sum([elt.match_key_values(['functor']) for elt in self._data if elt.functor in ACTANT_FUNCTORS], [])
        if key[0] == 'actant:form':
            return sum([elt.match_key_values(['functor:form']+key[1:]) for elt in self._data if elt.functor in ACTANT_FUNCTORS], [])
        else:
            return sum([elt.match_key_values(key[1:]) for elt in self._data if elt.functor == key[0]], [])

    def __str__(self):
        return ' '.join([str(el) for el in self.elements])

    def __json__(self, **opts):
        return {'elements': self._data, 'comments': self.comments}

    @classmethod
    def from_json(cls, dct):
        """
            Constructs a frame attribute from a simple dict.
        """
        ret = cls(data=dct['elements'])
        ret.comments = dct['comments']
        return ret

    @property
    def elements(self) -> List[FrameElement]:
        """
            The list of the frame elements.
        """
        return self._data or []


@json_register
class SpecvalElement:
    """
        A class representing a single element of the ``Specval`` attribute, i.e.
        an attribute specifying the diff between the frame of a noun and the frame
        of the verb it is derived from.

        Attributes:

            functor:    the functor (e.g. ``ORIG``)
            spec:       either of ``=``, ``+`` or ``-`` depending on whether the functor is
                        present in both the noun and the verb, only in the noun or only in the verb
                        respectively
            forms_add:  a list of forms present in the noun version but not in the verb one
            forms_del:  a list of forms present in the verb version but not in the noun one
            forms_eq:   a list of forms common to both the noun and the verb version
            oblig_noun: the obligatory type of the noun (e.g. ``opt``, ``obl``, ...)
            oblig_verb: the obligatory type of the verb (e.g. ``opt``, ``obl``, ...)

    """
    __slots__ = 'functor', 'spec', 'forms_typ', 'forms_eq', 'forms_add', 'forms_del', 'oblig_noun', 'oblig_verb'
    _SPEC2HUMAN = {
        '=': 'eq',
        '+': 'add',
        '-': 'del'
    }

    def __init__(self, functor: str, spec: str = '=',
                 forms_typ: Optional[List[Tuple[str, List[str]]]] = None,
                 forms_eq: Optional[List[str]] = None,
                 forms_add: Optional[List[str]] = None,
                 forms_del: Optional[List[str]] = None,
                 oblig_noun: Optional[str] = None, oblig_verb: Optional[str] = None):
        self.functor: str = functor
        self.spec = spec
        self.forms_add = forms_add or []
        self.forms_del = forms_del or []
        self.forms_eq = forms_eq or []
        self.forms_typ = forms_typ or []
        self.oblig_noun: str = oblig_noun or ''
        self.oblig_verb: str = oblig_verb or ''

    def match_key_values(self, key: List[str]) -> Iterable[str]:
        """
            Returns a list of strings which are matched when when searching the `key`
            (where `key` is either empty --- match against the full element, or
            ``oblig``, ``functor`` or ``forms`` in which case the matching is performed
            against the respective attribute)

            For more details on search see :module:`vallex.grep`.
        """
        if not key:
            return [str(self)]

        if key[0] in ['eq', 'add', 'del']:
            if self._SPEC2HUMAN[self.spec] != key[0]:
                return []
            return self.match_key_values(key[1:])

        if key[0] == 'oblig':
            if not key[1:]:
                return [self.oblig_noun, self.oblig_verb]
            if key[1] == 'changed':
                if self.spec == '=':
                    return [str(self.oblig_verb != self.oblig_noun)]
                else:
                    return []
            if key[1] == 'verb':
                return [self.oblig_verb]
            return [self.oblig_noun]

        if key[0] == 'functor':
            if not key[1:] or self._SPEC2HUMAN[self.spec] == key[1]:
                return [self.functor]
            return []

        if key[0] == 'functor:typ':
            if not key[1:] or self._SPEC2HUMAN[self.spec] == key[1]:
                return [self.functor+':'+'@'.join([verb+'->'+','.join(noun) for verb, noun in self.forms_typ])]
            return []

        if key[0] == 'form':
            if not key[1:]:
                return [verb+'->'+','.join(noun) for verb, noun in self.forms_typ]+self.forms_eq+self.forms_add+self.forms_del
            if key[1] == 'typ':
                return [verb+'->'+','.join(noun) for verb, noun in self.forms_typ]
            if key[1] == 'eq':
                return self.forms_eq
            if key[1] == 'add':
                return self.forms_add
            if key[1] == 'del':
                return self.forms_del

        return []

    def __str__(self):
        args = []
        if self.forms_typ:
            args.append('>:'+'@'.join([verb+'->'+','.join(noun) for verb, noun in self.forms_typ]))
        if self.forms_eq:
            args.append('=:'+','.join(self.forms_eq))
        if self.forms_add:
            args.append('+:'+','.join(self.forms_add))
        if self.forms_del:
            args.append('-:'+','.join(self.forms_del))
        args.append(self.oblig_verb+'->'+self.oblig_noun)
        return self.spec+self.functor + '('+';'.join(args)+')'

    def __eq__(self, other):
        if not isinstance(other, (FrameElement, SpecvalElement)):
            return False
        if self.functor != other.functor:
            return False

        if isinstance(other, SpecvalElement):
            if self.spec != other.spec:
                return False

            if set(self.forms_eq) != set(other.forms_eq) or \
               set(self.forms_add) != set(other.forms_add) or \
               set(self.forms_del) != set(other.forms_del) or \
               set([vf for vf, _ in self.forms_typ]) != set([vf for vf, _ in other.forms_typ]):
                return False

            self_ft = {vf: nfs for vf, nfs in self.forms_typ}
            other_ft = {vf: nfs for vf, nfs in other.forms_typ}
            for vf, nfs in self.forms_typ:
                if set(nfs).difference(set(other_ft[vf])):
                    return False

            if self.oblig_noun != other.oblig_noun or self.oblig_verb != other.oblig_verb:
                return False

            return True

        if self.spec == '+':
            return set(self.forms_add) == set(other.forms) and self.oblig_noun == (other.oblig or '')

        if self.spec == '-':
            return set(self.forms_del) == set(other.forms) and self.oblig_verb == (other.oblig or '')

        return not self.forms_add and \
            not self.forms_del and \
            self.oblig_noun == self.oblig_verb == (other.oblig or '') and \
            set(self.forms_eq) == set(other.forms)

    def __json__(self, **opts):
        return {
            'functor': self.functor, 'spec': self.spec,
            'forms_typ': [[vf, nf] for vf, nf in self.forms_typ], 'forms_eq': self.forms_eq, 'forms_add': self.forms_add, 'forms_del': self.forms_del,
            'oblig_noun': self.oblig_noun, 'oblig_verb': self.oblig_verb
        }

    @classmethod
    def from_json(cls, dct):
        """
            Constructs a specval element from a simple dict.
        """
        return SpecvalElement(**dct)


@json_register
class Specval(Attrib):
    """
        A class representing the valdiff attribute
        i.e. an attribute specifying the diff between the
        frame of a noun and the frame of the verb it is derived from. It consists of a list
        of :class:`SpecvalElement` elements, each element corresponding to an added, deleted or changed
        functor.

        Attributes:

            _data:              list of specval elements
            TYPICAL_CHANGES     changes in forms which are considered typical and, hence, uninteresting
    """

    TYPICAL_CHANGES = {
        '1': ['2', '7', 'pos', 'od+2'],
        '4': ['2', 'pos'],
        '2': ['2', 'pos'],
        '3': ['2', 'pos'],  # TODO: these changes are non-systemic in case of velení-1 and velení-3; now there is a workaround in the add_valdiff transform
        'jako+1': ['jako+2'],
        'jako+4': ['jako+2'],
        'jako+adj-4': ['jako+adj-2']
    }

    def __init__(self, attr_name: str = 'valdiff', data: Optional[List[SpecvalElement]] = None):
        super().__init__(attr_name, data)  # type: ignore

    def match_keys(self):
        """
            Returns a list of valid match_keys against which a search may be
            performed (see :module:`vallex.grep` for more information on
            how searching is implemented.).
        """
        ret = [
            ('valdiff', 'list of (computed) specval slot sources'),
            ('valdiff.src', 'source text of the (computed) specval'),
            ('valdiff.comments', 'comments on the (computed) specval'),
            ('valdiff.functor', 'list of all functors of the noun or verb'),
            ('valdiff.functor.eq', 'list of all functors common to the noun and verb'),
            ('valdiff.functor.add', 'list of all functors added in the noun'),
            ('valdiff.functor.del', 'list of all functors missing in the noun'),
            ('valdiff.functor:typ', 'list of all typical changes (functor:verb_form->noun_forms) in common functors'),
            ('valdiff.actant', 'list of all actant functors of the noun or verb'),
            ('valdiff.actant.eq', 'list of all actant functors common to the noun and verb'),
            ('valdiff.actant.add', 'list of all actant functors added in the noun'),
            ('valdiff.actant.del', 'list of all actant functors missing in the noun'),
            ('valdiff.form', 'list of all forms in common functors of the noun or verb'),
            # TODO: Perhaps change valdiff.form.typ to return (vform->nform) strings (i.e.
            # one such string for each nform given a single vform, instead of all the nforms
            # joined by a comma...)
            ('valdiff.form.typ', 'list of all typical changes (verb_form->noun_forms) in common functors'),
            ('valdiff.form.eq', 'list of all unchanged forms in common functors'),
            ('valdiff.form.add', 'list of all added forms in in common functors'),
            ('valdiff.form.del', 'list of all deleted forms in in common functors'),
            ('valdiff.actant.form', 'list of all forms in common  actant functors of the noun or verb'),
            ('valdiff.actant.form.eq', 'list of all unchanged forms in common actant functors'),
            ('valdiff.actant.form.add', 'list of all added forms in in common actant functors'),
            ('valdiff.actant.form.del', 'list of all deleted forms in in common actant functors'),
            ('valdiff.oblig', 'list of all obligatory types in all functors of the noun or verb'),
            ('valdiff.oblig.noun', 'the obligatory types of the derived noun'),
            ('valdiff.oblig.verb', 'the obligatory types of the source verb'),
            ('valdiff.oblig.changed', 'True/False depending on whether the obligatory type changed in either of the functors'),
        ]
        functor_keys = [
            ('valdiff.'+slot.functor, 'source of the '+slot.functor+' slots of the noun or verb', slot) for slot in self._data
        ]+[
            ('valdiff.'+slot.functor+'.eq', 'source of the '+slot.functor+' slot common to the noun and verb', slot) for slot in self._data if slot.spec == '='
        ]+[
            ('valdiff.'+slot.functor+'.add', 'source of the '+slot.functor+' slot added in the noun', slot) for slot in self._data if slot.spec == '+'
        ]+[
            ('valdiff.'+slot.functor+'.del', 'source of the '+slot.functor+' slot missing in the noun', slot) for slot in self._data if slot.spec == '-'
        ]
        ret.extend([fk[:2] for fk in functor_keys])
        ret.extend([
            (fk[0]+'.form', fk[1].replace('source of the', 'list of forms of the')) for fk in functor_keys
        ])
        ret.extend([
            (fk[0]+'.form.typ', fk[1].replace('source of the', 'list of typical changes of the')) for fk in functor_keys if fk[2].spec == '='
        ])
        ret.extend([
            (fk[0]+'.form.eq', fk[1].replace('source of the', 'list of common forms of the')) for fk in functor_keys if fk[2].spec == '='
        ])
        ret.extend([
            (fk[0]+'.form.add', fk[1].replace('source of the', 'list of added forms of the')) for fk in functor_keys if fk[2].spec == '='
        ])
        ret.extend([
            (fk[0]+'.form.del', fk[1].replace('source of the', 'list of missing forms of the')) for fk in functor_keys if fk[2].spec == '='
        ])
        ret.extend([
            (fk[0]+'.oblig', fk[1].replace('source of the', 'obligatory types of the')) for fk in functor_keys
        ])
        ret.extend([
            (fk[0]+'.oblig.changed', fk[1].replace('source of the', 'True/False based on whether oblig. type of the')+'changed') for fk in functor_keys if fk[2].spec == '='
        ])
        ret.extend([
            (fk[0]+'.oblig.verb', fk[1].replace('source of the', 'obligatory type of the verb of the')) for fk in functor_keys if fk[2].spec == '='
        ])
        ret.extend([
            (fk[0]+'.oblig.noun', fk[1].replace('source of the', 'obligatory type of the derived noun of the')) for fk in functor_keys if fk[2].spec == '='
        ])
        return ret

    def match_key_values(self, key: List[str]) -> Iterable[str]:
        """
            Returns a list of strings which are matched when when searching the `key`
            (for the list of available keys see :meth:`Specval.match_keys`).

            For more details on search see :module:`vallex.grep`.
        """
        if not key:
            return [str(slot) for slot in self._data]
        if key[0] == 'src':
            return [str(self)]
        if key[0] == 'comments':
            return sum([c.match_key_values([]) for c in self.all_comments], [])
        if key[0] in ['functor', 'functor:typ']:
            return sum([elt.match_key_values(key) for elt in self._data], [])
        if key[0] in ['actant']:
            if key[1:] and key[1] == 'form':
                return sum([elt.match_key_values(key[1:]) for elt in self._data if elt.functor in ACTANT_FUNCTORS and elt.spec == '='], [])
            return sum([elt.match_key_values(['functor']+key[1:]) for elt in self._data if elt.functor in ACTANT_FUNCTORS], [])
        if key[0] in ['form', 'oblig']:
            return sum([elt.match_key_values(key) for elt in self._data if elt.spec == '='], [])
        return sum([elt.match_key_values(key[1:]) for elt in self._data if elt.functor == key[0]], [])

    @classmethod
    def diff(cls, verb_frame: Frame, noun_frame: Frame, changeset=TYPICAL_CHANGES) -> 'Specval':
        """
            A method to create a specval attribute from a verb frame and a corresponding noun frame.
        """
        verb_functs = {elt.functor for elt in verb_frame.elements}  # type: ignore
        noun_functs = {elt.functor for elt in noun_frame.elements}  # type: ignore
        common = [elt.functor for elt in noun_frame.elements if elt.functor in verb_functs]
        added = noun_functs.difference(common)
        deleted = verb_functs.difference(common)
        add_elts = [SpecvalElement(elt.functor, spec='+', forms_add=elt.forms, oblig_noun=elt.oblig) for elt in noun_frame.elements if elt.functor in added]  # type: ignore
        # deleted typical complementations may ignored
        del_elts = [SpecvalElement(elt.functor, spec='-', forms_del=elt.forms, oblig_verb=elt.oblig) for elt in verb_frame.elements if elt.functor in deleted and elt.oblig != "typ"]  # type: ignore
        common_elts = []
        for common_functor in common:
            v_elt = [elt for elt in verb_frame.elements if elt.functor == common_functor][0]  # type: ignore
            n_elt = [elt for elt in noun_frame.elements if elt.functor == common_functor][0]  # type: ignore
            common_forms = set(v_elt.forms).intersection(set(n_elt.forms))
            add_forms = set(n_elt.forms).difference(common_forms)
            del_forms = set(v_elt.forms).difference(common_forms)
            typical_changes = []
            if common_functor in ACTANTS_AND_CPHR:
                for src, tgt in changeset.items():
                    if src in del_forms.union(common_forms) and add_forms.union(common_forms).intersection(tgt):
                        ch = (src, [form for form in n_elt.forms if form in add_forms.union(common_forms).intersection(tgt)])
                        typical_changes.append(ch)
                del_forms.difference_update({src for src, _ in typical_changes})
                common_forms.difference_update({src for src, _ in typical_changes if src in _})
                for _, tgt in typical_changes:
                    add_forms.difference_update(tgt)
            elif common_functor == "DPHR":  # FIXME: if DPHR.form.add begins with same 5chars as DPHR.form.del, consider it a typical change
                for src in del_forms.union(common_forms):
                    corresponding_tgts = []  # type: List[str]
                    for form in add_forms.union(common_forms):  # type: str
                        if src[0:4] == form[0:4]:
                            corresponding_tgts.append(form)
                    if corresponding_tgts != [src]:  # form that just stays the same is not a change
                        ch = (src, corresponding_tgts)
                        typical_changes.append(ch)
                common_forms.difference_update({src for src, _ in typical_changes if src in _})
                del_forms.difference_update({src for src, _ in typical_changes})
                for _, tgt in typical_changes:
                    add_forms.difference_update(tgt)

            common_elts.append(SpecvalElement(common_functor, spec='=',
                                              forms_typ=typical_changes,
                                              forms_eq=[form for form in n_elt.forms if form in common_forms],
                                              forms_add=[form for form in n_elt.forms if form in add_forms],
                                              forms_del=[form for form in v_elt.forms if form in del_forms],
                                              oblig_noun=n_elt.oblig,
                                              oblig_verb=v_elt.oblig))
        return Specval(data=common_elts+add_elts+del_elts)

    def __eq__(self, other):
        if not isinstance(other, Specval):
            return False
        self_elt_map = {elt.functor: elt for elt in self._data}
        other_elt_map = {elt.functor: elt for elt in other._data}
        if set(self_elt_map.keys()) != set(other_elt_map.keys()):
            return False
        for funct, elt in self_elt_map.items():
            if elt != other_elt_map[funct]:
                return False
        return True

    def __str__(self):
        return ' '.join([str(el) for el in self._data])
