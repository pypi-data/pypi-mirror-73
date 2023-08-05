""" A helper module for de/serializing Python objects to JSON.



    This module contains variants of the methods found in :mod:`json`
    which know how to deal with objects representing Lexical Units,
    Lexemes, Attributes and other data structures mainly found in the
    :mod:`vallex.data_structures` module. Additionally it contains
    a decorator which is used to decorate objects which need to be
    handled by these methods.
"""
import json


_TYPE_MAP = {}
"""
    Contains a mapping from type-names into the actual classes. This
    is used for constructing objects of the appropriate type (given
    by the ``__type__`` key) from JSON dicts. It is populated by
    the :func:`register` decorator.
"""


def register(cls):
    """
        A decorator to make classes with a ``__json__`` method and
        ``from_json`` classmethod JSON-serializable.

        The ``__json__`` method should return a python :class:`dict`.
        The dict should not contain the '__type__' key (which will
        be overwritten by the object class name in order that we later
        know how to deserialize it)

        The ``from_json`` class method should construct an instance
        of the class given a dict produced by the ``__json__`` method.
    """
    _TYPE_MAP[cls.__name__] = cls
    return cls


def _json2obj(dct):
    obj_type = dct.get('__type__', None)
    if obj_type in _TYPE_MAP:
        del dct['__type__']
        return _TYPE_MAP[obj_type].from_json(dct)
    return dct


def _encoder(opts):
    class _CustomJSONEncoder(json.JSONEncoder):
        def default(self, obj):
            if hasattr(obj, '__json__'):
                ret = obj.__json__(**opts)
                ret['__type__'] = type(obj).__name__
                return ret

            # Let the base class default method raise the TypeError
            return json.JSONEncoder.default(self, obj)
    return _CustomJSONEncoder


def dump(db, OUT, indent=2, **opts):
    """
        A variant of the standard :func:`json.dump` function which knows
        how to handle Lexicon-related objects.
    """
    json.dump(db, OUT, cls=_encoder(opts), indent=indent, sort_keys=True, ensure_ascii=False)


def dumps(db, indent: bool = None, **opts) -> str:
    """
        A variant of the standard :func:`json.dumps` function which knows
        how to handle Lexicon-related objects.
    """
    return json.dumps(db, cls=_encoder(opts), indent=indent)


def load(IN):
    """
        A variant of the standard :func:`json.load` function which knows
        how to handle Lexicon-related objects.
    """
    return json.load(IN, object_hook=_json2obj)


def loads(src: str):
    """
        A variant of the standard :func:`json.loads` function which knows
        how to handle Lexicon-related objects.
    """
    return json.loads(src, object_hook=_json2obj)
