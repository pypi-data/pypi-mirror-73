import re

from vallex import Attrib


def compute_isNoun(lu):
    attr = Attrib('isNoun', dynamic=True, help='Is it a noun (True/False)?', data='blu-n' in lu._id)
    lu.dynamic_attrs[attr.name] = attr


def compute_isVerb(lu):
    attr = Attrib('isVerb', dynamic=True, help='Is it a verb (True/False)?', data='blu-v' in lu._id)
    lu.dynamic_attrs[attr.name] = attr


REFLVERB_RGX = re.compile(r'.*T[12]?\s+S[IE].*')
"""A regexp for recognizing reflexive verbs from the id of their parent lexeme."""


def compute_isReflexverb(lu):
    attr = Attrib('isReflexverb', dynamic=True, help='Is it a reflexive verb (True/False)?')
    attr._data = bool(lu._parent and REFLVERB_RGX.match(lu._parent._id))
    lu.dynamic_attrs[attr.name] = attr


def compute_productive(lu):
    if 'blu-n' in lu._id:
        attr = Attrib('productive', dynamic=True, help='Is it a productive noun (True/False)?')
        attr._data = True
        for var in ['', '1', '2', '3', '4']:
            if 'no-aspect'+var in lu.lemma._data.keys():
                attr._data = False
                break
        lu.dynamic_attrs[attr.name] = attr
