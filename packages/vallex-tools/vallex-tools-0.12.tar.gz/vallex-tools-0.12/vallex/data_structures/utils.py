""" This file contains definitions of helper classes.





    This module contains three classes:

    - :class:`AttrAccessor` a convenience class for allowing chained attribute access
    - :class:`Ref` represents a pointer/reference to another element
    - :class:`Text` represents a block of text
    - :class:`Comment` represents a single comment

    which are used as helper classes in other data structures.
"""
from functools import wraps
from typing import Iterable, List, Optional

from ..json_utils import register as json_register


def _must_override(meth):
    """
        A wrapper to ensure that the AttrAccessor implementation
        of the given method is not called for classes inheriting
        from :class:`AttrAccessor` having their :attr:`__val` equal to ``self``
    """
    @wraps(meth)
    def wrapped(self, *args, **kwargs):
        if self._val_is_self:
            raise TypeError("Classes inheriting from AttrAccessor must override "+meth.__name__+" if they want it defined.")
        return meth(self, *args, **kwargs)
    return wrapped


class AttrAccessor:
    """
        A utility class using Python Black Magic for converting chained
        attribute access (e.g. var.a.b.c.d) into a lookup call and
        returning None (instead of raising an exception), if lookup fails.

        Example Usage::

            def dict_resolver(d):
                def resolver(key):
                    ret = d
                    for k in key:
                        ret = ret[k]
                    return ret
                return resolver

            d = {'a':
                    {'b':
                        {'c': [0, 1, 2]}
                    }
            }
            acc = AttrAccessor(d, dict_resolver(d))
            assert acc.a.b.c[1] == 1
            assert not acc.a.b.c.d.e
            assert not acc.a.q

        It is inherited by the base :class:`Attrib <vallex.data_structures.attribs.Attrib>` and
        :class:`LexicalUnit <vallex.data_structures.lexical_unit.LexicalUnit>` classes whose
        lookup is based on the `match_key_values` methods.

        An AttrAccessor is a thin wrapper around its :attr:`__val` attribute which intercepts
        failed attribute access and tries to resolve these using the :attr:`__resolver` method.
        The resolver method will receive as its parameter a list of keys (the attribute chain)
        and should return a value corresponding to this chain.

        Note: When a class inherits :class:`AttrAccessor` and calls :class:`AttrAccessor`'s constructor with
        itself as value, it must also pass the `value_is_self` argument and set it to ``True``,
        otherwise calling some methods will lead to infinite recursion.

        Note: For understanding how the implementation works, understanding Python's
        `data model <https://docs.python.org/3/reference/datamodel.html>`_ isrequired.
    """
    @classmethod
    def _invalid_resolver(cls, x):
        raise AttributeError

    def __init__(self, value, subresolver, value_is_self=False, cached_value_provided=True):
        """
            Warning: If `value` is equal to `self`, it is mandatory to pass the `value_is_self`
            argument and set it to True
        """
        self.__resolver = subresolver
        self.__val = value
        self._val_is_self = value_is_self
        self.__cached = cached_value_provided

    def __bool__(self):
        # This is needed to prevent infinite recursion
        if self._val_is_self:
            return True
        return bool(self.deref)

    def __eq__(self, other):
        # This is needed to prevent infinite recursion
        if self._val_is_self:
            return id(other) == id(self.__val)
        return self.deref.__eq__(other)

    __getitem__ = _must_override(lambda self, key: self.deref[key])
    __len__ = _must_override(lambda self: len(self.deref))
    __str__ = _must_override(lambda self: self.deref.__str__())
    __or__ = _must_override(lambda self, other: self.deref.__or__(other))
    __and__ = _must_override(lambda self, other: self.deref.__and__(other))
    __add__ = _must_override(lambda self, other: self.deref.__add__(other))
    __mul__ = _must_override(lambda self, other: self.deref.__mul__(other))
    __div__ = _must_override(lambda self, other: self.deref.__div__(other))
    __hash__ = _must_override(lambda self: self.deref.__hash__())

    @property
    def deref(self):
        if not self.__cached:
            try:
                self.__val = self.__resolver()
            except:
                return None
        return self.__val

    def __getattr__(self, attr):
        # This method is called only if the standard
        # lookup fails (e.g. it is not called when
        # looking up ``__resolver``, ``__val`` and other
        # attributes explicitly set or defined on the class
        # See https://docs.python.org/3/reference/datamodel.html

        # Workaround for attribute lookup when resolver can deal
        # with attribute names which python forbids (e.g. class)
        if attr in ['class_', 'def_', 'for_', 'del_']:
            attr = attr[:-1]

        def subresolver(x=None): return self.__resolver([attr]+x) if x else self.__resolver([attr])
        return AttrAccessor(None, subresolver, cached_value_provided=False)


@json_register
class Ref:
    """
        Represents a reference to another element (e.g. LexicalUnit).
    """
    __slots__ = '_id', '_type'

    def __init__(self, id_: str, target_type: str = ''):
        self._id = id_
        self._type = target_type

    def __eq__(self, other):
        if type(other).__name__ == self._type:
            return self._id == other._id
        if isinstance(other, Ref):
            return self._id == other._id and self._type == other._type
        return False

    def __repr__(self):
        return self._type+'*(' + self._id + ')'

    def __str__(self):
        return self._id

    def __json__(self, **opts):
        return {'id': self._id, 'target_type': self._type}

    @classmethod
    def from_json(cls, dct):
        """
            Constructs a reference from a simple dict.
        """
        return Ref(dct['id'], dct['target_type'])


@json_register
class Text:
    """
        Represents a block of text.

        Currently does no more than keep the text as a string and a list of comments.

        TODO: It is envisioned, that it can contain additional data (e.g. word
        annotations, ...)

        Attributes:

            content:    A string containing the text
            _comments:  A list of comments.
    """
    __slots__ = 'content', 'comments'

    def __init__(self, txt: str = '', comments: Optional[List['Comment']] = None):
        self.content = txt
        if comments:
            self.comments = comments
        else:
            self.comments = []

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.content)

    def __len__(self):
        return len(self.content)

    def __eq__(self, other):
        if isinstance(other, Text):
            if not self.content == other.content:
                return False
            return set(self.comments) == set(other.comments)
        if isinstance(other, str):
            return self.content == other
        return False

    def __add__(self, other):
        if isinstance(other, str):
            return Text(self.content+other, self.comments)
        if isinstance(other, Text):
            return Text(self.content+other.content, self.comments + other.comments)
        raise NotImplementedError

    def __iadd__(self, other):
        if isinstance(other, str):
            self.content += other
        elif isinstance(other, Text):
            self.content += other.content
            self.comments += other.comments
        return self

    def find(self, needle: str):
        return self.content.find(needle)

    def strip(self, *args, **kwargs):
        return Text(self.content.strip(*args, **kwargs), self.comments)

    def __json__(self, **opts):
        return {'content': self.content, 'comments': self.comments}

    @classmethod
    def from_json(cls, dct):
        """
            Constructs a Text instance from a simple dict.
        """
        return Text(dct['content'], dct['comments'])


@json_register
class Comment:
    """
        Represents a comment.

        Currently does no more than keep the text of the comment as a string.

        TODO: Implement author association & threading (replies, ...)

        Attributes:

            content:    A string containing the text

    """
    __slots__ = ('content', )

    def __init__(self, content: str = ''):
        self.content: str = content

    def __str__(self):
        return self.content

    def __eq__(self, other):
        return isinstance(other, Comment) and other.content == self.content

    def __json__(self, **opts):
        return {'content': self.content}

    def match_key_values(self, key: List[str]) -> Iterable[str]:
        return [self.content]

    @classmethod
    def from_json(cls, dct):
        """
            Constructs a comment from a simple dict.
        """
        return Comment(dct['content'])
