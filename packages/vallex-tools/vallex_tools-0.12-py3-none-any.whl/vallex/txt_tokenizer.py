""" Tokenizer for the Vallex txt format



    This file implements the :class:`TokenStream` class which
    represents Vallex data in the txt format as a list of
    Tokens of various kinds (see the descendants of the :class:`Token`
    class below).

    This is then used by the parser in :mod:`vallex.txt_parser`
    to generate a list of parsed lexemes.
"""
import hashlib
import re

# from collections import defaultdict
from typing import Iterable, Type, Optional, List, Union

from .error import LocatedError
from .location import Location


class EOSException(LocatedError):
    pass


class StreamIndexError(IndexError):
    pass


class InvalidToken(LocatedError):
    def __init__(self, token, src, location):
        super().__init__("Invalid token: "+repr(token), src, location)
        self._token = token


class Token:
    """
        The root of the class hiearchy of tokens. Every token
        type must derive from this class. Additionally, when
        defining a new token type, one must register it with
        TokenFactory using the TokenFactory.register_token
        decorator.

        Attributes:
            _src:   contains the part of the source string which was converted into
                    the token
            _loc:   the location in the source where the token started
            _val:   the "value" of the token (has different interpretations
                    for different token types)
    """
    TOKEN_NAME = 'UNKNOWN TOKEN'
    """A human readable token name (printed in error messages, etc.)"""

    def __init__(self, src: str = '', val: str = '', location: Location = None):
        self._src = src
        self._loc = location
        self._val = val

    @classmethod
    def parse(cls, src: str, loc: Location) -> Optional['Token']:
        """
            Tries parsing the source `src` into the token.

            Returns:
                The new instance of the token if successful, None otherwise
        """

    def __eq__(self, other):
        return type(self) == type(other) and self._val == other._val

    def __len__(self):
        return len(self._src)

    def __str__(self):
        return str(self._val)

    def __repr__(self):
        return '<'+self.TOKEN_NAME+'('+str(self._val)+')>'


class TokenFactory:
    """
        Used by the :class:`TokenStream` class to split the source into a list of tokens
        by calling the static method :meth:`TokenFactory.next_token` every time it wants
        to parse the next token from the source.
    """
    REGISTERED_TOKENS: List[Token] = []
    """
        Contains a list of registered token classes. When parsing tokens,
        the ``parse`` method of each class is tried in order and the
        first one that succeeds creates the next token.
    """

    # STATS = {
    #    'counts': [],
    #    'type_counts': defaultdict(int),
    #    'total_toks': 0
    # }
    # Used for profiling

    @classmethod
    def next_token(cls, src: str, loc: Location) -> Optional[Token]:
        """
            Iterates over all registered tokens and calls their parse
            method on `src`. The first successful parse is returned.

            Returns:
                The next token in the source `src`, None if there are no more tokens.
        """
        count = 0
        for tok_type in cls.REGISTERED_TOKENS:
            count += 1
            tok = tok_type.parse(src, loc)
            if tok:
                if tok._src.endswith('\n') and not isinstance(tok, Newline):
                    tok._src = tok._src[:-1]
                #  cls.STATS['counts'].append(count)
                #  cls.STATS['total_toks'] += 1
                #  cls.STATS['type_counts'][tok.TOKEN_NAME] += 1
                return tok
        #  cls.STATS['counts'].append(count)
        #  cls.STATS['total_toks'] += 1
        #  cls.STATS['type_counts']['UNKNOWN'] += 1
        return None

    @classmethod
    def register_token(cls, tok_name: str):
        """
            Registers a token class named `tok_name`.

            Note: The order in which the tokens are registered is important!
                  In particular, some of the RegExp-based tokens rely on the
                  fact that no previous reg-exp token matched.
        """
        def decorator(tok_cls):
            tok_cls.TOKEN_NAME = tok_name
            cls.REGISTERED_TOKENS.append(tok_cls)
            return tok_cls
        return decorator


class RegExpParser:
    """
        Mixin class providing a method to parse a token given a regular expression
        as the REGEX attribute of the class.
    """

    REGEX = re.compile('')
    """
        The regular expression defining the token. It should contain a single
        named group ``value``. This group will be the token's value.
    """

    @classmethod
    def parse(cls, src, loc: Location) -> Optional[Token]:
        """
            Tries parsing the source `src` into the token.

            Returns:
                The new instance of the token if successful, None otherwise
        """
        m = cls.REGEX.match(src, pos=loc.pos)
        if m:
            spos, epos = m.span()
            return cls(src[spos:epos], m.groupdict()['value'].strip(), loc)  # type: ignore
        return None


class CharClassParser:
    """
        Mixin class providing a method to parse a token given a list of characters.
    """
    CHAR_CLASS = ''
    """Any character in the class is converted into a token."""

    @classmethod
    def parse(cls, src, loc: Location) -> Optional[Token]:
        """
            Tries parsing the source `src` into the token.

            Returns:
                The new instance of the token if successful, None otherwise
        """
        if src[loc.pos] in cls.CHAR_CLASS:
            return cls(src[loc.pos], src[loc.pos], loc)  # type: ignore
        return None


@TokenFactory.register_token('NEWLINE')
class Newline(CharClassParser, Token):
    """Represents a newline character."""
    CHAR_CLASS = '\n'

    def __init__(self, src='\n', val='\n', loc=None):
        super().__init__(src, val, loc)


@TokenFactory.register_token('WHITESPACE')
class WhiteSpace(Token):
    """Represents a continuous sequence of whitespace characters
       (not including newline characters, these have their own
       token class :class:`Newline`)
    """
    WHITESPACE = ' \t\r\f\v'

    @classmethod
    def parse(cls, src, loc) -> Optional[Token]:
        # AV: why not r'WHITESPACE*' ?
        # JV thinks that this may be quicker than using regex
        whitespace = ''
        pos = loc.pos
        tot_len = len(src)
        while pos < tot_len and src[pos] in cls.WHITESPACE:
            whitespace += src[pos]
            pos += 1
        if whitespace:
            return cls(whitespace, whitespace, loc)
        return None

    def __str__(self):
        return ' '


@TokenFactory.register_token('LEXEME START')
class LexemeStart(RegExpParser, Token):
    """Token starting a lexeme."""
    REGEX = re.compile(r'\*\s(?P<value>[^#\n]+)(?=(#[^\n]*)?\n)')
    # REGEX = re.compile(r'\*\s(?P<value>[^#\n]+)')


@TokenFactory.register_token('LU START')
class LexicalUnitStart(RegExpParser, Token):
    """Token starting a lexical unit."""
    REGEX = re.compile(r':\s*id:\s+(?P<value>\S+)\s*(?=(#[^\n]*)?\n)')
    # REGEX = re.compile(r':\s*id:\s+(?P<value>\S+)')


@TokenFactory.register_token('LEMMA')
class Lemma(Token):
    """Token starting the lemma attribute of a lexical unit."""

    @classmethod
    def parse(cls, src, loc) -> Optional[Token]:
        if src[loc.pos:loc.pos+2] == '~ ':
            return cls(loc=loc)
        return None

    def __init__(self, src='~ ', val='~', loc=None):
        super().__init__(src, val, loc)


@TokenFactory.register_token('FRAME')
class Frame(Token):
    """Token starting the frame attribute of a lexical unit."""

    @classmethod
    def parse(cls, src, loc) -> Optional[Token]:
        if src[loc.pos:loc.pos+2] == '+ ':
            return cls(loc=loc)
        if src[loc.pos:loc.pos+3] == '+i ':
            return cls(src='+i ', val='+', loc=loc)
        return None

    def __init__(self, src='+ ', val='+', loc=None):
        super().__init__(src, val, loc)


@TokenFactory.register_token('LU ATTRIBUTE')
class LexicalUnitAttr(RegExpParser, Token):
    """
        Token starting other lexical unit attributes.

        The value of the token is the attribute name.
    """
    REGEX = re.compile(r'-(?P<value>[\w-]+):[ \t]*')


@TokenFactory.register_token('VID')
class Vid(RegExpParser, Token):
    """Token representing an aspect."""
    VIDY = ['pf', 'impf', 'iter', 'no-aspect', 'biasp']
    REGEX = re.compile(r'(?P<value>'+r'|'.join([v+r'[1234]?' for v in VIDY])+r'):\s')


FUNCTORS = [
    'ACMP', 'ACT', 'ADDR', 'ADVS', 'AIM', 'APP', 'APPS', 'ATT', 'AUTH', 'BEN', 'CAUS',
    'CNCS', 'COMPL', 'COND', 'CONFR', 'CONJ', 'CPHR', 'CPR', 'CRIT', 'CSQ', 'CTERF',
    'DENOM', 'DES', 'DIFF', 'DIR', 'DIR1', 'DIR2', 'DIR3', 'DISJ', 'DPHR', 'EFF',
    'ETHD', 'EXT', 'FPHR', 'GRAD', 'HER', 'ID', 'INTF', 'INTT', 'LOC', 'MANN', 'MAT',
    'MEANS', 'MOD', 'NA', 'NONE', 'NORM', 'OBST', 'ORIG', 'PAR', 'PARTL', 'PAT', 'PN',
    'PREC', 'PRED', 'RCMP', 'REAS', 'REG', 'RESL', 'RESTR', 'RHEM', 'RSTR', 'SENT',
    'SUBS', 'TFHL', 'TFRWH', 'THL', 'THO', 'TOWH', 'TPAR', 'TSIN', 'TTILL', 'TWHEN',
    'VOC', 'VOCAT', 'EMPTY'
]
"""The list of valid functors."""

FUNCTOR_RGX_SRC = r'('+r'|'.join(['[-+=]?'+f for f in FUNCTORS])+r')'
"""Regexp matching valid functors."""

FUNCTOR_TUPLE_RGX_SRC = r'(' + FUNCTOR_RGX_SRC + r'-?){1,3}'
"""Regexp matching groups of two or three valid functors joined by ``-``."""


@TokenFactory.register_token('VALENCY SLOT')
class ValencySlot(Token):
    """
        A Token representing a functor with arguments in parentheses.

        The value of the token is the functor, the :attr:`_args`
        contains the arguments (everything inside the parentheses)
    """
    REGEX = re.compile(r'(?P<functor>'+FUNCTOR_TUPLE_RGX_SRC+r')\((?P<args>[^\)]*)\)')
    _args: str = ''

    @classmethod
    def parse(cls, src, loc):
        m = cls.REGEX.match(src, pos=loc.pos)
        if m:
            capt = m.groupdict()
            spos, epos = m.span()
            tok = cls(src[spos:epos], capt['functor'], loc)
            tok._args = capt['args']
            return tok
        return None

    def __str__(self):
        return self._val+"("+self._args+")"


@TokenFactory.register_token('SCOPE')
class FunctorCombination(RegExpParser, Token):
    """
        A token representing a combination of up to three functors joined by a ``+`` character
        and followed by a colon (``:``); the token typically indicates that the following
        examples exemplify the functor combination.
    """
    REGEX = re.compile(r'(?P<value>('+FUNCTOR_RGX_SRC+r'\+?){1,3}):\s')


@TokenFactory.register_token('LIST OF FUNCTOR TUPLES')
class FunctorTupleList(RegExpParser, Token):
    """
        A token representing a ``,``-separated list of functor combinations.
    """
    REGEX = re.compile(r"(?P<value>" + FUNCTOR_TUPLE_RGX_SRC + r"(?:,\s " + FUNCTOR_TUPLE_RGX_SRC + r")*)")


@TokenFactory.register_token('COMMENT')
class Comment(RegExpParser, Token):
    """
        A token representing a comment.
    """
    REGEX = re.compile(r'#(?P<value>[^\n]*)\n')


@TokenFactory.register_token('SEPARATOR')
class Percent(CharClassParser, Token):
    CHAR_CLASS = '%'

    def __init__(self, src='%', val='%', loc=None):
        super().__init__(src, val, loc)


@TokenFactory.register_token('SEPARATOR')
class Comma(CharClassParser, Token):
    CHAR_CLASS = ','

    def __init__(self, src=',', val=',', loc=None):
        super().__init__(src, val, loc)


@TokenFactory.register_token('SEPARATOR')
class Semicolon(CharClassParser, Token):
    CHAR_CLASS = ';'

    def __init__(self, src=';', val=';', loc=None):
        super().__init__(src, val, loc)


@TokenFactory.register_token('OPEN_PAREN')
class OpenParen(CharClassParser, Token):
    CHAR_CLASS = '('

    def __init__(self, src='(', val='(', loc=None):
        super().__init__(src, val, loc)


@TokenFactory.register_token('CLOSE_PAREN')
class CloseParen(CharClassParser, Token):
    CHAR_CLASS = ')'

    def __init__(self, src=')', val=')', loc=None):
        super().__init__(src, val, loc)


@TokenFactory.register_token('PIPE')
class Pipe(CharClassParser, Token):
    CHAR_CLASS = '|'

    def __init__(self, src='|', val='|', loc=None):
        super().__init__(src, val, loc)


@TokenFactory.register_token('QUOTE')
class Quote(CharClassParser, Token):
    """
        A token representing a quote.

        Note:   The source text only contains ASCII quotes
                (i.e. ``'`` and ``"``) so we use heuristics to determine
                whether the token is actually an opening or a closing
                quote.

        Attributes:
            _open:  indicates whether the quote is an opening or a closing quote.

    """
    CHAR_CLASS = '"\''
    _open: Optional[bool] = None

    def set_open(self, state: bool = True):
        """
            The :meth:`set_open` is used to indicate whether the
            quote is an opening or a closing quote.
        """
        self._open = state

    def __str__(self):
        """
            The __str__ method returns the correct form of the quote depending
            on whether it is an opening of a closing quote.
        """
        if self._open is not None:
            if self._open:
                if self._val == '"':
                    return '„'
                return "‚"
            if self._val == '"':
                return '“'
            return "‘"
        return str(self._val)


@TokenFactory.register_token('IDENTIFIER')
class Identifier(RegExpParser, Token):
    """
        A token representing a lexical unit id.
    """
    REGEX = re.compile(r'(?P<value>@?[\w]+-[\w+.-]*\w+)')


@TokenFactory.register_token('AUGMENTED WORD')
class AugmentedWord(Token):
    """
        A token representing a word with a functor specification.
    """
    REGEX = re.compile(r'(?P<word>\w+)\.(?P<augment>' + FUNCTOR_TUPLE_RGX_SRC + ')')
    _augment: str = ''

    @classmethod
    def parse(cls, src, loc):
        m = cls.REGEX.match(src, pos=loc.pos)
        if m:
            capt = m.groupdict()
            spos, epos = m.span()
            tok = cls(src[spos:epos], capt['word'], loc)
            tok._augment = capt['augment']
            return tok
        return None

    def __str__(self):
        return str(self._val)+'.'+str(self._augment)


@TokenFactory.register_token('WORD')
class Word(RegExpParser, Token):
    """
        A token representing a single word.
    """
    REGEX = re.compile(r'(?P<value>\w+)')


class EndOfSource(Token):
    """
        A token representing the end of the source (typically
        the End Of File)
    """
    TOKEN_NAME = 'END OF SOURCE'


class Other(Token):
    """
        A token representing a character not represented by the previous tokens.
    """
    TOKEN_NAME = 'OTHER'


class TokenStream(Iterable[Token]):
    """
        Parses source data into an iterable sequence of tokens.
        where each token is a triple::

            (token_type, value, source_location)

        with token_type being the type of the token, value its value
        and source_location its location in the source...
    """

    def __init__(self, src: str, fname: Optional[str] = ''):
        self.src = src
        self._checksum = hashlib.sha512(bytes(self.src, encoding='utf-8')).hexdigest()
        self.loc = Location(self.src, filename=fname, pos=0, ln=0, col=0)
        self.left: List[Token] = []

    def push_left(self, token: Token) -> None:
        """
            Puts a new token in front of the remaining source.
        """
        self.loc = token._loc.clone()  # type: ignore
        self.left.append(token)

    def pop_left(self) -> Token:
        """
            Returns the next token in the source, removing it in the process.
        """
        return next(self)

    def peek(self) -> Token:
        """
            Returns the next token in the source, without removing it in the process.
        """
        return self._next_tok(advance=False)

    def cat_until(self, token_types: Union[List[Type], Type], invalid_token_types: Optional[Union[List[Type], Type]] = None) -> List[Token]:
        """
            Scans the stream until the first token of type present in `token_types` is found.
            Returns the list of tokens up to (and not including) that point.
        """
        if not isinstance(token_types, list):
            token_types = [token_types]
        if invalid_token_types is None:
            invalid_token_types = []
        if not isinstance(invalid_token_types, list):
            invalid_token_types = [invalid_token_types]
        toks: List[Token] = []

        for tok in self:
            if type(tok) in token_types:
                self.push_left(tok)
                return toks
            if type(tok) in invalid_token_types:
                raise InvalidToken(tok, src=self.src, location=tok._loc)
            toks.append(tok)
        raise EOSException("End of stream while looking for TOKENS "+str([t.TOKEN_NAME for t in token_types]), src=self.src, location=self.loc)

    def cat_while(self, token_types: Union[List[Type], Type]) -> List[Token]:
        """
            Scans the stream until the first token of type not present in `token_types` is found.
            Returns the list of tokens up to (and not including) that point.
        """
        if not isinstance(token_types, list):
            token_types = [token_types]
        ret = []
        tok = next(self)
        while type(tok) in token_types:
            ret.append(tok)
            tok = next(self)
        self.push_left(tok)
        return ret

    def _next_tok(self, advance=True) -> Token:
        if self.left:
            if advance:
                ret_tok = self.left.pop(0)
                self.loc._inc_pos(len(ret_tok))
                if isinstance(ret_tok, Newline):
                    self.loc._newline()
                return ret_tok
            return self.left[0]

        old_loc = self.loc.clone()
        if self.loc.pos == len(self.src):
            if advance:
                self.loc._inc_pos()
            return EndOfSource(location=old_loc)
        if self.loc.pos > len(self.src):
            raise StreamIndexError

        tok = TokenFactory.next_token(self.src, old_loc)
        if tok:
            if advance:
                self.loc._inc_pos(len(tok))
                if isinstance(tok, Newline):
                    self.loc._newline()
            return tok

        if advance:
            self.loc._inc_pos()
        return Other(src=self.src[old_loc.pos], val=self.src[old_loc.pos], location=old_loc)

    def __len__(self):
        return max(len(self.left)+len(self.src)-self.loc.pos, 0)

    def seek(self, loc: Location) -> None:
        self.left = []
        self.loc = loc

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self._next_tok(advance=True)
        except StreamIndexError:
            raise StopIteration


def split(tokens: Iterable[Token], sep_tok_types: Union[List[Type], Type], include_separators=True) -> List[Union[List[Token], Token]]:
    """
        Splits the list of `tokens` into sublists separated by tokens whose type is in `sep_tok_types`.
        If include_separators is True, it works somewhat like re.split, e.g. the separators are also returned among
        the sublists (as lists of size one).

        Returns:
             A list of sublists of `tokens` where each element is either empty, is a list
             containing just one token whose type is in `sep_tok_types` or is a list of tokens
             whose types are not in `sep_tok_types`. Any two lists of the first or last type
             are separated by a list of the second type.
    """
    if not isinstance(sep_tok_types, list):
        sep_tok_types = [sep_tok_types]
    ret: List[Union[List[Token], Token]] = []
    curr: List[Token] = []
    for tok in tokens:
        if type(tok) in sep_tok_types:
            ret.append(curr)
            if include_separators:
                ret.append(tok)
            curr = []
        else:
            curr.append(tok)
    ret.append(curr)
    return ret


def join(tokens: Iterable[Token], sep=' '):
    """
        Converts a list of tokens into a list of strings and then
        concatenates these strings using `sep`.
    """
    return sep.join([str(t) for t in tokens])
