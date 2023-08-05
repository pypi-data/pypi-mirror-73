""" Definitions of Exceptions & Errors.



    This module provides definitions related to error handling.


"""
import logging

from typing import Optional, Union

from .location import Location
from .log import log


class LocatedError(Exception):
    """
        A Base class for exceptions tied to a specific location in a source.

        Used mainly by the :mod:`.txt_parser` and :mod:`.txt_tokenizer` modules
        when coming across parsing errors. When converted to str it shows
        the message together with a short excerpt from the source (
        with `context_lines` number of context lines).

        Attributes:
            loc(:class:`.location.Location`): describes the location in source where the error happened.
            message(str):                     an error message describing the exception
            context_lines(int):               the number of context lines to print
    """

    def __init__(self, message, src: str = '', location: Optional[Union[Location, int]] = None):
        super().__init__(message)
        if isinstance(location, Location):
            self.loc = location
        elif isinstance(location, int):
            if src is None:
                self.loc = Location(pos=location)
            else:
                self.loc = Location.location_from_pos(src, location)
        else:
            self.loc = Location(src)
        self.message = message
        self.context_lines = 4

    def __str__(self):
        lines = []
        lines.append(type(self).__name__+" at "+str(self.loc)+": "+self.message)
        lines.extend(self.loc.context(num_ctx_lines=self.context_lines))
        return "\n".join(lines)


class UnknownFormat(Exception):
    pass


DATA_ERRORS = []
"A list of errors encountered during parsing. This is populated by the :func:`data_error` function."

MISSING_ATTR = 0
"The lexical unit is missing a required attribute"

UNHANDLED_ATTR = 1
"The parser encountered an attribute which it doesn't know how to parse."

UNBALANCED_QUOTES = 2
"Quotes should come in pairs"

UNEXPECTED_TOKEN = 3
"The parser encountered an unexpected token"

DUPLICATE_ATTR = 4
"A lexical unit should not have duplicate attributes"

INVALID_ATTR_VALUE = 5
"An attribute which has an invalid value"

INVALID_ATTR = 6
"An invalid attribute"

ERROR_NAMES = {
    MISSING_ATTR: 'Missing mandatory attribute',
    UNHANDLED_ATTR: 'Unknown attribute',
    UNBALANCED_QUOTES: 'Unbalanced quotes in text',
    UNEXPECTED_TOKEN: 'Unexpected token when parsing',
    DUPLICATE_ATTR: 'Attribute already specified',
    INVALID_ATTR_VALUE: 'Invalid attribute value',
    INVALID_ATTR: 'Invalid attribute name'
}


def data_error(component, error_type: int, loc: Optional[Location], *message):
    if error_type not in ERROR_NAMES.keys():
        raise Exception("Unknown error type", error_type)
    log('data.'+component, logging.WARN, *message, "at", loc)
    DATA_ERRORS.append((loc, error_type, message))
