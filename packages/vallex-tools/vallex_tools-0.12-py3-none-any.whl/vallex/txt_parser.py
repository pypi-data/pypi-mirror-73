""" Contains functions to parse lexicon data in txt format




    Parsing the lexicon data is done using the :func:`parse` function
    in two steps:

    1. In the first step, the input string (file) is converted
       into a stream of tokens (using the :class:`TokenStrea <.txt_tokenizer.TokenStream>`
       class).

    2. In the second step (in function :func:`parse_token_stream`), this stream
       is iterated over and whenever a :class:`LexemeStart <.txt_tokenizer.LexemeStart>`
       token is encountered, a single Lexeme is parsed (using the :func:`parse_lexeme`)
       and added to the collection of parsed lexemes.

    The second step is implemented via the :func:`parse_lexeme`, :func:`parse_lexical_unit`
    and :func:`parse_attr` functions. Since the attributes have a lot of variability
    in terms of their structure (some are plain values, some are lists, some contain links,
    ...) the function :func:`parse_attr` calls specialized functions which must be
    implemented separately for the different type of attributes. These functions take
    two arguments --- the head token (an instance of :class:`LexicalUnitAttr <.txt_tokenizer.LexicalUnitAttr>`)
    and a list of tokens comprising the body of the attribute. They each return an instance
    of :class:`Attrib <.data_structures.attribs.Attrib>` representing the parsed attribute.

    When implementing a parser for a new attribute, this parser needs to be decorated
    using the :meth:`AttributeFactory.register_parser` decorator, which is passed
    the list of attribute names as its argument, e.g.::

        @AttributeFactory.register_parser('examplerich', 'example', 'example1', ...)
        def parse_example(head, body):
            ...

    Typically, one will also implement a subclass of :class:`Attrib <.data_structures.attribs.Attrib>`
    to represent a new attribute (and put it into the :mod:`.data_structures.attribs` package),
    however this is not strictly necessary.

    Currently the following parsers are implemented:

    - :func:`parse_note`
    - :func:`parse_example`
    - :func:`parse_recipr`
    - :func:`parse_reflist` (lvc-type attributes)
    - :func:`synon`

    Other attributes will raise a warning (``error.INVALID_ATTR``) during parsing and will
    be processed by a general parser which just makes the `_data` attr contain the source
    of the attribute body.
"""

import io

from typing import Callable, Dict, Iterable, List, Optional, Tuple, Union

from . import error
from . import txt_tokenizer as tok
from .error import data_error
from .data_structures import Attrib, Comment, Frame, FrameElement, Lemma, Lexeme, LexicalUnit, Lexicon, Ref, Specval, SpecvalElement, Text


def parse(src: Union[str, io.IOBase], fname: Optional[str] = None) -> Lexicon:
    """
        Parses a txt-formatted lexicon.

        .. deprecated:: 0.5
           Use :func:`parse_token_stream` instead.
    """
    if isinstance(src, str):
        text = src
    else:
        text = src.read()  # type: ignore
    stream = tok.TokenStream(text, fname=getattr(src, 'name', ''))
    lexicon = parse_token_stream(stream)
    lexicon.path = fname
    return lexicon


def parse_token_stream(stream: tok.TokenStream, progress_cb: Optional[Callable[[int, int], None]] = None) -> Lexicon:
    """
        Parses the token stream `stream` into a collection of Lexemes.

        Note:
            1.  The stream represents a lexicon, in particular it might start
                with some comments which do not belong to any lexemes. This is
                dealt with by storing every comment that is encountered before
                the first lexeme in the preamble of the returned collection.
            2.  Comments which are on separate lines in between lexemes are
                always saved with the lexeme that immediately preceded them
                (the parser has no way to know if they should belong to the
                next lexeme or not); similarly comments between lexical units
                are automatically attached to the preceding lu
            3.  Parsing errors are reported via the :func:`data_error <.error.data_error>`
                function and ignored otherwise (i.e. the parser does its best
                to continue parsing).

        Todo:
            The error handling/reporting should be rethought.
    """
    preamble = [Comment(str(c)) for c in stream.cat_until([tok.LexemeStart, tok.EndOfSource]) if isinstance(c, tok.Comment)]

    # If present, strip the preamble we put in automatically when converting to txt
    if preamble and preamble[0].content.startswith('START ========== ') and preamble[0].content.endswith(' ========== START'):
        preamble = preamble[2:]
    ret = []
    count = 0
    while stream:
        stream.cat_until([tok.LexemeStart, tok.EndOfSource])
        if isinstance(stream.peek(), tok.EndOfSource):
            break
        ret.append(parse_lexeme(stream))
        count += 1
        if progress_cb and count % 20 == 0:
            progress_cb(stream.loc.pos, count)

    # If present, strip the postamble we put in automatically when converting to txt
    if ret and ret[-1].lexical_units:
        last_attr = list(ret[-1].lexical_units[-1].attribs.values())[-1]
        last_comments = last_attr.comments.get('all', [])
        if last_comments and last_comments[-1].content.startswith('END ========== ') and last_comments[-1].content.endswith(' ========== END'):
            last_comments.pop()
            last_comments.pop()

    lexicon = Lexicon(ret, preamble)
    lexicon._checksum = stream._checksum
    return lexicon


def parse_lexeme(stream: tok.TokenStream) -> Lexeme:
    """
        Parses one lexeme from the stream of tokens `stream`.

        Notes
        -----

        1. The function assumes that the first token of the stream
           is an :class:`LexemeStart <.txt_tokenizer.LexemeStart>` token.
        2. Tokens comprising the lexeme are consumed.
    """
    start_tok = stream.pop_left()
    lex = Lexeme(start_tok._val)  # type: ignore
    lex._src_start = start_tok._loc.clone()  # type: ignore

    for token in stream:
        if isinstance(token, tok.LexicalUnitStart):
            stream.push_left(token)
            lex.lexical_units.append(parse_lexical_unit(stream, lex))
        elif isinstance(token, tok.Comment):
            lex.comments.append(Comment(str(token)))
        elif isinstance(token, tok.LexemeStart):
            stream.push_left(token)
            lex._src_end = token._loc.clone()   # type: ignore
            return lex
        elif isinstance(token, tok.EndOfSource):
            lex._src_end = token._loc.clone()  # type: ignore
            return lex
        elif isinstance(token, (tok.WhiteSpace, tok.Newline)):
            continue
        else:
            data_error("parser:txt", error.UNEXPECTED_TOKEN, token._loc, "Expecting", tok.LexemeStart.TOKEN_NAME+",", tok.LexicalUnitStart.TOKEN_NAME, "or", tok.EndOfSource.TOKEN_NAME, "found", str(token), 'instead')
            stream.cat_until([tok.LexicalUnitStart, tok.LexemeStart, tok.Comment, tok.EndOfSource])
    lex._src_end = stream.loc.clone()
    return lex


def parse_lexical_unit(stream: tok.TokenStream, parent: Lexeme) -> LexicalUnit:
    """
        Parses one lexical unit from the list of tokens `stream`.

        Example
        -------

        A typical lexical unit might look like::

            : id: blu-v-brát-vzít-1
            ~ impf: brát (si) pf: vzít (si) iter: brávat (si)
            + ACT(1;obl) PAT(4;obl) ORIG(od+2;opt) LOC(;typ) DIR1(;typ) RCMP(za+4;typ)
                -synon: impf: přijímat; získávat pf: přijmout; získat
                -example: impf: brát si od někoho mzdu / peníze za práci; vláda nebude mít odkud peníze brát; brát si snídani
                        pf: vzal si od něj peníze za práci; vláda nebude mít odkud peníze vzít; vzít si snídani
                -note: mohli loni brát na odměnách.COMPL měsíčně 26 až 40 tisíc korun
                    volné si
                -recipr: impf: ACT-ORIG %berou si od sebe peníze%
                        pf: ACT-ORIG %nikdy si od sebe nevzali peníze%

                ...

        The first line is the header of the lu and contains its id. It
        is represented in the token stream by a :class:`LexicalUnitStart <.txt_tokenizer.LexicalUnitStart>`
        token.

        The next two lines comprise the mandatory attributes which
        each lu must have: the lemma (the line started by ``~``) and the frame (the line
        started by ``+``). These are represented in the stream as
        a :class:`Lemma <.txt_tokenizer.Lemma>` token, followed by a list of tokens ended with a
        :class:`Newline <.txt_tokenizer.Newline>` token and, respectively, a
        :class:`Frame <.txt_tokenizer.Frame>` token, again followed by a list of tokens ending
        with a :class:`Newline <.txt_tokenizer.Newline>`.

        Finally, the remaining lines (until another :class:`LexicalUnitStart <.txt_tokenizer.LexicalUnitStart>`,
        :class:`LexemeStart <.txt_tokenizer.LexemeStart>` or :class:`EndOfSource <.txt_tokenizer.EndOfSource>`
        are parsed as attributes of the lexical unit, each attribute starting with a
        :class:`LexicalUnitAttr <.txt_tokenizer.LexicalUnitAttr>` token ending with the next such token
        or a token starting a new lu, lexeme or indicating the end of file.


        Notes
        -----

        1. The function assumes that the first token of the stream
           is an :class:`LexemeStart <.txt_tokenizer.LexemeStart>` token.
        2. Tokens comprising the lexeme are consumed.
        3. The parser does not assume that the frame and lemma attribute lines are in order
           or that there are no intervening lines (although in practice the ordering
           shown in the above example and without intervening lines can be expected).

    """

    start_tok = stream.pop_left()
    lu = LexicalUnit(start_tok._val, parent)  # type: ignore
    lu._src_start = start_tok._loc.clone()  # type: ignore

    # Parse the mandatory attributes
    mandatory_attrs = [tok.Lemma, tok.Frame]
    invalid_tokens = [tok.LexicalUnitStart, tok.LexemeStart, tok.EndOfSource, tok.LexicalUnitAttr]
    mandatory_attrs_preparsed = {}
    while mandatory_attrs:
        try:
            mattr_start = stream.loc.clone()
            lu.comments.extend([Comment(str(t)) for t in stream.cat_until(mandatory_attrs, invalid_token_types=invalid_tokens) if isinstance(t, tok.Comment)])
        except tok.InvalidToken:
            data_error("parser:txt", error.MISSING_ATTR, lu._src_start, "Missing mandatory attributes", [m.TOKEN_NAME for m in mandatory_attrs], "for lexical_unit", lu._id)
            stream.seek(mattr_start)
            break
        attr_head = stream.pop_left()
        val = stream.cat_until(tok.Newline)
        attr_comments = [Comment(str(t)) for t in val if isinstance(t, tok.Comment)]
        val = [t for t in val if not isinstance(t, tok.Comment)]
        mandatory_attrs_preparsed[attr_head._val] = val, attr_comments
        mandatory_attrs.remove(type(attr_head))

        # WTF?? Who came up with this notation???
        if '+i' in attr_head._src:
            lu.attribs['idiom'] = Attrib('idiom', True)

    # Parse the lemma
    if '~' in mandatory_attrs_preparsed:
        val, comments = mandatory_attrs_preparsed['~']
        lu.lemma = Lemma(data=parse_keyval(val, stringify_vals=True)[0])
        lu.lemma.comments = {'all': comments}

    # Parse the frame
    if '+' in mandatory_attrs_preparsed:
        val, comments = mandatory_attrs_preparsed['+']
        lu.frame = parse_frame(val)
        lu.frame.comments = {'all': comments}

    # Parse the optional attributes
    stop_set = [tok.LexicalUnitStart, tok.LexemeStart, tok.EndOfSource, tok.LexicalUnitAttr]
    while stream:
        stream.cat_until(stop_set)
        if not isinstance(stream.peek(), tok.LexicalUnitAttr):
            lu._src_end = stream.loc.clone()
            return lu
        attr = parse_attr(stream)
        if attr.name in lu.attribs:
            if attr.name != 'note':
                data_error("parser:txt", error.DUPLICATE_ATTR, lu._src_start, "Attribute", attr.name, "already defined here:", str(lu.attribs[attr.name]._src_start), "for lexical_unit", lu._id)
            attr.duplicate, attr.name = attr.name, _generate_name(attr.name, lu.attribs.keys())
            if attr.name == '':
                data_error("parser:txt", error.DUPLICATE_ATTR, lu._src_start, "Unable to find unique name for Attribute", attr.duplicate, "for lexical_unit", lu._id)
        lu.attribs[attr.name] = attr
    lu._src_end = stream.loc.clone()
    return lu


def _generate_name(base: str, forbidden: Iterable[str]) -> str:
    """
        Tries to generate a new attribute name for a duplicate attribute
        by iteratively appending a character to `base` and testing if its not
        contained in `forbidden`.
    """
    for uniq in '0123456789ABCDEFGHIJKLMNOPQRSTUVXYZ':
        if base+'-'+uniq not in forbidden:
            return base+uniq
    return ''


def parse_keyval(tokens: List[tok.Token], stringify_vals=False) -> Tuple[Dict[str, Union[str, List[tok.Token]]], Dict[str, List[Comment]]]:
    """
        Parses a list tokens which consists of (scoped token/vid, value) pairs into a dictionary.
        The value will typically be a list of tokens. For example::

            Vid(impf) Word(chodit) Newline() Vid(pf) Word(dojít) Vid(iter) Word(hvízdat) Word(si)

        corresponding to source::

            impf: chodit
            pf: dojít iter: hvízdat si

        will be converted into::

            {'impf': 'chodit', 'pf': 'dojít', 'iter': 'hvízdat si'}

        Args:
            tokens: the list of tokens to parse
            stringify_vals: whether to convert tokens into strings when returning.

        Returns:
            The resulting pairs as a dictionary keyed by the stringified value of the first element
            and the values being either directly the second elements (a list of tokens) if stringify_vals is False or a
            concatenation of the stripped stringified values of the second element.
    """
    ret: Dict[str, Union[str, List[tok.Token]]] = {}
    comments = {}

    # This method does bulk of the work by splitting
    # such that the even elements are keys and the odd elements are values
    # (except perhaps the first...)
    parts = tok.split(tokens, [tok.FunctorCombination, tok.Vid])

    # When the first element is not an empty list, this indicates that the list started with a value
    # without a key (e.g. the value applies to all keys). In this case we store it under the
    # special key 'all'.
    if parts[0]:
        if stringify_vals:
            val = ''.join([str(v) for v in parts[0] if not isinstance(v, tok.Comment) and str(v)])   # type: ignore
            ret['all'] = val
        else:
            ret['all'] = [v for v in parts[0] if not isinstance(v, tok.Comment)]   # type: ignore
        comments['all'] = [Comment(v._val) for v in parts[0] if isinstance(v, tok.Comment)]   # type: ignore

    # Discard the first element (either it was empty or we took care of it above)
    parts = parts[1:]

    # Iterate over the (key, value) pairs and store them in the ret dictionary
    for i in range(int(len(parts)/2)):
        key = parts[2*i]
        if stringify_vals:
            val = ''.join([str(v) for v in parts[2*i+1] if not isinstance(v, tok.Comment) and str(v)])   # type: ignore
            ret[str(key)] = val
        else:
            ret[str(key)] = [v for v in parts[2*i+1] if not isinstance(v, tok.Comment)]   # type: ignore
        comments[str(key)] = [Comment(v._val) for v in parts[2*i+1] if isinstance(v, tok.Comment)]  # type: ignore
    return ret, comments


class AttributeFactory:
    """
        Used by the :func:`parse_attr` function to parse a head_token and a list of body tokens
        into a lexical unit attribute (an instance of :class:`Attrib <.data_structures.attribs.Attrib>`).
        This is done by the :meth:`AttributeFactory.parse_attribute`
        class (static) method; This method delegates the actual parsing to parser methods registered using
        the :meth:`AttributeFactory.register_parser` class (static) method.
    """

    REGISTERED_ATTRIBUTES: Dict[str, Callable[[tok.Token, List[tok.Token]], Attrib]] = {}
    "Contains a mapping from attribute names to functions used to parse them"

    VALID_ATTRIBUTE_NAMES = [
        'alternations', 'class', 'control', 'conv',
        'derived', 'derivedN', 'derivedV',  # TODO: test that 'derived' is not used - it should be one of the other two
        'diat',
        'example', 'examplerich', 'example1', 'example2', 'example3', 'example4', 'example5', 'example6', 'example7',
        'full',
        'instig', 'instig1', 'instig2', 'instig3', 'instig4', 'instig5', 'instig6', 'instig7',
        'limit',
        'lvc', 'lvc1', 'lvc2', 'lvc3', 'lvc4', 'lvc5', 'lvc6', 'lvc7', 'lvcN', 'lvcV',
        'map', 'map1', 'map2', 'map3', 'map4', 'map5', 'map6', 'map7',
        'multiple', 'note', 'otherforms', 'pdt-vallex',
        'recipr', 'recipr1', 'recipr2', 'recipr3', 'reciprevent', 'reciprtype', 'reciprverb', 'reflex',
        'specval', 'split', 'status', 'synon', 'type', 'use',
        # and for Polish data also:
        'ref'
    ]
    "A list of all valid attribute names"

    @classmethod
    def parse_attribute(cls, head_token: tok.Token, body_token_list: List[tok.Token]) -> Attrib:
        """
            Creates a lexical unit attribute (an instance of :class:`Attrib <vallex.data_structures.attribs.Attrib>`)
            from a `head_token` and the body `body_token_list` (a list of tokens).
        """
        attr_name = head_token._val
        if attr_name in cls.REGISTERED_ATTRIBUTES:
            return cls.REGISTERED_ATTRIBUTES[attr_name](head_token, body_token_list)

        if attr_name not in cls.VALID_ATTRIBUTE_NAMES:
            data_error("parser:txt", error.INVALID_ATTR, head_token._loc, "Invalid attribute type", attr_name)
        else:
            data_error("parser:txt", error.UNHANDLED_ATTR, head_token._loc, "Unhandled attribute type", attr_name)
        attr = Attrib(attr_name)   # type: ignore
        attr._data = ''.join([t._src for t in body_token_list if not isinstance(t, tok.Comment)]).strip()
        attr.comments = {'all': [Comment(str(t)) for t in body_token_list if isinstance(t, tok.Comment)]}
        return attr

    @classmethod
    def register_parser(cls, *args):
        """
            A decorator which registers a parser method for attributes whose name is in the `*args` list.
        """
        def decorator(parser_method):
            for arg in args:
                cls.REGISTERED_ATTRIBUTES[arg] = parser_method
            return parser_method
        return decorator


def parse_attr(stream: tok.TokenStream) -> Attrib:
    """
        Parses a single attribute of a lexical unit from the token stream `stream`.

        The bulk of the work is done by calling :meth:`AttributeFactory.parse_attribute` which in turn
        calls parsers for the various attributes.

        Returns:
            The parsed attribute.
    """

    # Get the attribute name
    head = next(stream)
    src_start = head._loc.clone()

    # Get the body of the attribute
    body = stream.cat_until([tok.LexicalUnitStart, tok.LexemeStart, tok.EndOfSource, tok.LexicalUnitAttr])
    src_end = stream.loc.clone()

    attr = AttributeFactory.parse_attribute(head, body)
    attr._src_start = src_start
    attr._src_end = src_end
    return attr


def process_text(tok_list: List[tok.Token]) -> Text:
    """
        Converts a list of tokens into a Text object.

        Replaces ASCII quotes with corresponding open/close quotes.
    """
    ret = Text()

    open_quotes: List[tok.Quote] = []
    for token in tok_list:
        if isinstance(token, tok.Quote):
            if not open_quotes:
                token.set_open(True)
                open_quotes.append(token)
            else:
                if open_quotes[-1]._val == token._val:
                    token.set_open(False)
                    open_quotes.pop()
                else:
                    token.set_open(True)
                    open_quotes.append(token)

        if isinstance(token, tok.Comment):
            ret.comments.append(Comment(str(token)))
        else:
            ret += str(token)

    if open_quotes:
        data_error('parser:txt', error.UNBALANCED_QUOTES, open_quotes[0]._loc, 'Unbalanced quote starting')

    ret.content = ret.content.strip()

    return ret


def parse_frame(body) -> Frame:
    """
        Parses the body of the frame attribute.

        Example:
            A typical frame attribute might look like::

                + ACT(1;obl) PAT(4;obl) ORIG(od+2;opt) LOC(;typ) DIR1(;typ) RCMP(za+4;typ)

            The token corresponding to the '+' is not a part of the body, the rest of the line
            would be tokenized by the tokenizer as a list of :class:`.txt_tokenizer.ValencySlot`
            tokens::

                [ValencySlot('ACT', '1;obl'), ValencySlot('PAT', '4;obl'), ValencySlot('ORIG', 'od+2;obl'), ...]

            (or :class:`.txt_tokenizer.FunctorTupleList` in case the functor does not
            have any forms or oblig, i.e. stands alone without parentheses) whose
            :attr:`_val <.txt_tokenizer.Token._val>` attributes will be the
            functor name (e.g. ``'ACT'``) and whose :attr:`_args <.txt_tokenizer.Token._args>`
            attribute will contain the string inside the parentheses (e.g. ``'1;obl'``).

            TODO: it would be better to represent the Valency Slot as a 3-tuple
            consisting of functor, forms and obligatoriness
    """

    elts = []
    for token in body:
        if isinstance(token, tok.FunctorTupleList):
            if ' ' in token._val:
                data_error('parser:txt', error.INVALID_ATTR_VALUE, token._loc, 'Invalid functor name', token._val, 'while parsing frame')
            else:
                elts.append(FrameElement(token._val, [], None))
        elif str(token).strip().upper() == 'TODO':
            elts.append(FrameElement(str(token).strip(), [], None))
        elif isinstance(token, tok.ValencySlot):
            if ';' in token._args:
                forms, oblig = token._args.split(';', maxsplit=2)
                forms = forms.split(',')  # type: ignore
                if oblig not in ['obl', 'opt', 'typ']:
                    data_error('parser:txt', error.INVALID_ATTR_VALUE, token._loc, 'Invalid obligatory type', oblig, 'while parsing frame')
            else:
                forms, oblig = token._args.split(','), None  # type: ignore
            elts.append(FrameElement(token._val, forms, oblig))  # type: ignore
        elif isinstance(token, tok.WhiteSpace):
            pass
        else:
            data_error('parser:txt', error.UNEXPECTED_TOKEN, token._loc, 'Unexpected token', token._val, 'while parsing frame')
    return Frame(data=elts)


@AttributeFactory.register_parser('valdiff')
def parse_specval(_, body) -> Specval:
    """
        Parses the body of the specval attribute.

        Example:
            A specval attribute might look like (not a real-world example)::

                -specval: =ACT(=:1,add+4,2;->) =PAT(=:2;+:3,po+4;-:1,po+3;pat->opt) +LOC(+:4,za+5,2;->obl) -ADDR(-:4,za+5,2;obl->)

            The body would be tokenized by the tokenizer as a list of :class:`.txt_tokenizer.ValencySlot`
            tokens::

                [ValencySlot('=ACT', '=:1,add+4,2;->'), ValencySlot('=PAT', '=:2;+:3,po+4;-:1,po+3;pat->opt'),  ...]

            (or :class:`.txt_tokenizer.FunctorTupleList` in case the functor does not
            have any forms or oblig, i.e. stands alone without parentheses) whose
            :attr:`_val <.txt_tokenizer.Token._val>` attributes will be the
            functor name (e.g. ``'ACT'``) preceded by an action symbol (``=``, ``+``, or ``-``) and whose :attr:`_args <.txt_tokenizer.Token._args>`
            attribute will contain the string inside the parentheses (e.g. ``'=:1,add+4,2;->'``). This string
            is a collection of ``;``-separated substrings, with the last item of the from ``verb_oblig->noun_oblig`` (``verb_oblig`` is the verb
            obligatory type or empty if not specified and ``noun_oblig`` is the noun obligatory type or empty if not specified). The previous
            items are of the form ``act:forms`` where ``act`` is an action symbol (``=``, ``+``, or ``-``) and ``forms`` is a ``,``-separated
            list of forms.
    """
    elts = []
    for token in body:
        if isinstance(token, tok.FunctorTupleList):
            if ' ' in token._val:
                data_error('parser:txt', error.INVALID_ATTR_VALUE, token._loc, 'Invalid functor value', token._val, 'while parsing specval')
            else:
                if token._val[0] == '+':
                    elts.append(SpecvalElement(token._val[1:], spec='+'))
                elif token._val[0] == '-':
                    elts.append(SpecvalElement(token._val[1:], spec='-'))
                elif token._val[0] == '=':
                    elts.append(SpecvalElement(token._val[1:], spec='='))
                else:
                    data_error('parser:txt', error.INVALID_ATTR_VALUE, token._loc, 'Expected action (=,+, or -) got', token._val, 'instead while parsing specval')
        elif isinstance(token, tok.ValencySlot):
            args = token._args.split(';')
            oblig_verb, oblig_noun = args[-1].split('->')
            if oblig_verb not in ['obl', 'opt', 'typ', '']:
                data_error('parser:txt', error.INVALID_ATTR_VALUE, token._loc, 'Invalid obligatory type (verb)', oblig_verb, 'while parsing specval')
            if oblig_noun not in ['obl', 'opt', 'typ', '']:
                data_error('parser:txt', error.INVALID_ATTR_VALUE, token._loc, 'Invalid obligatory type (noun)', oblig_noun, 'while parsing specval')
            forms: Dict[str, List[str]] = {
                '=': [],
                '+': [],
                '-': []
            }
            typical: List[Tuple[str, List[str]]] = []
            for group in args[:-1]:
                act, data = group.split(':')
                if act not in ['=', '+', '-', '>']:
                    data_error('parser:txt', error.INVALID_ATTR_VALUE, token._loc, 'Invalid action type', act, 'while parsing specval')
                elif act == '>':
                    typical = [(ch.split('->')[0], ch.split('->')[1].split(',')) for ch in data.split('@')]
                else:
                    forms[act] = data.split(',')
            elts.append(SpecvalElement(token._val[1:], spec=token._val[0],
                                       forms_typ=typical,
                                       forms_eq=forms['='],
                                       forms_add=forms['+'],
                                       forms_del=forms['-'],
                                       oblig_verb=oblig_verb, oblig_noun=oblig_noun))
        elif isinstance(token, tok.WhiteSpace):
            pass
        else:
            data_error('parser:txt', error.UNEXPECTED_TOKEN, token._loc, 'Unexpected token', token._val, 'while parsing frame')
    return Specval(data=elts)


@AttributeFactory.register_parser('note')
def parse_note(head, body) -> Attrib:
    """
        Parses the note attribute

        Returns:
            The parsed attribute whose :attr:`_data <.data_structures.attribs.Attrib._data>` attribute contains
            the content of the note as a simple string.
    """
    attr = Attrib(str(head))
    attr._data = [''.join([t._src for t in body]).strip()]
    return attr


@AttributeFactory.register_parser('examplerich', 'example', 'example1', 'example2', 'example3', 'example4', 'example5', 'example6', 'example7')
def parse_example(head, body) -> Attrib:
    """
        Parses an example-type attribute.

        The body of the example attribute consists of a list of exemplifying sentences
        separated by semicolons. Some sentences may be relevant for the whole lexical
        unit, while others may exemplify just a specific aspect. This latter case is
        indicated by prefixing the examples with the name of the aspect followed by a colon.
        For example the following source::

            -example2: impf: Od cizinců mají zakázáno brát úplatky.;
                            Podle dřívějších informací ho policisté viní z toho, že si jeho společnost brala úvěry od společností sídlících na britském ostrově Man a v Nizozemsku.;
                    pf: Zkraje 80. let prý vzal úplatek od Japonců.;
                        Ještě to neřeším, ale samozřejmě si budeme muset vzít překlenovací úvěr.

        has a list of four example sentences with the first two exemplifying the ``impf`` aspect
        while the latter two exemplify the ``pf`` aspect.

        Returns:
            The parsed attribute whose :attr:`_data <.data_structures.attribs.Attrib._data>` is a dictionary
            keyed by aspect names which contains a list of sentences (instances of the
            :class:`Text <.data_structures.utils.Text>` class) exemplifying each aspect.
    """
    attr = Attrib(str(head))
    attr._data = {}

    parsed_data, attr.comments = parse_keyval(body)
    data = {k: tok.split(v, tok.Semicolon, include_separators=False) for k, v in parsed_data.items()}  # type: ignore
    for key, val in data.items():
        attr._data[key] = list(filter(None, [process_text(ex) for ex in val]))  # type: ignore

    return attr


@AttributeFactory.register_parser('recipr', 'recipr1', 'recipr2', 'recipr3')
def parse_recipr(head, body) -> Attrib:
    """
        Parses the recipr attribute.

        The body of the recipr attribute resembles the example attribute, except that
        the exemplifying sentences are relevant not just to a given aspect, but also
        for a given functor combination (i.e. there are two levels)::

            -recipr: impf: ACT-ADDR %děti si berou hračky navzájem%
                     pf: ACT-ADDR %vzali si navzájem peníze%

        Also, the examples are enclosed in ``%`` characters instead of being separated
        by the semicolon.

        Returns:
            The parsed attribute whose :attr:`_data <.data_structures.attribs.Attrib._data>` is a dictionary
            keyed by aspect names which contains a further dictionary keyed by functor names which
            finally contains a list of exemplifying sentences (instances of the
            :class:`Text <.data_structures.utils.Text>` class).

        TODO:
            The implementation should be revisited by someone more familiar with the
            lexicon format to ensure its correctness and coherence.
    """
    attr = Attrib(str(head))
    attr._data = {}

    parsed_data, attr.comments = parse_keyval(body)

    data = {vid: tok.split(per_vid_data, tok.FunctorTupleList) for vid, per_vid_data in parsed_data.items()}  # type: ignore
    for vid, per_vid_data in data.items():
        per_vid_final = {}

        # When the first element is not an empty list, this indicates that we start with an unqualified example
        if per_vid_data[0]:
            all_ = list(filter(None, [process_text(ex) for ex in tok.split(per_vid_data[0], tok.Percent, include_separators=False)]))  # type: ignore
            if all_:  # FIXME: This should not happen, we should probably look at parsed_data.items() and do some filtering
                per_vid_final['all'] = all_

        per_vid_data = per_vid_data[1:]
        for i in range(int(len(per_vid_data)/2)):
            tgt_list = per_vid_data[2*i]
            examples = list(filter(None, [process_text(ex) for ex in tok.split(per_vid_data[2*i+1], tok.Percent, include_separators=False)]))  # type: ignore
            per_vid_final[str(tgt_list)] = examples

        attr._data[vid] = per_vid_final

    return attr


@AttributeFactory.register_parser('lvc', 'lvcN', 'lvcV', 'derivedN', 'derivedV', 'lvc1', 'lvc2', 'lvc3', 'lvc4', 'lvc5', 'lvc6', 'lvc7',
                                  # for Polish data also:
                                  'ref')
def parse_reflist(head, body) -> Attrib:
    """
        Parses the lvc-type attributes.

        The body of a lvc-type attribute consists of a space (or comma) separated list of lexical unit ids, optionally
        followed by ``|`` and a list of space separated lemmata , e.g.::

             -lvc: blu-n-chyba-1 blu-n-gesto-1 blu-n-kompromis-1 ...  blu-n-závěr-2 | narážka rozdíl

        Returns:
            The parsed attribute whose :attr:`_data <.data_structures.attribs.Attrib._data>` is a dictionary
            which contains, under the ``ids`` key, the list of lu references (instances of the
            :class:`Ref <.data_structures.utils.Ref>` class) and, under the ``lemmas`` key, the list
            of lemmas (pure strings).
    """
    attr = Attrib(str(head))
    attr._data = {'ids': [], 'lemmas': []}

    # Extract comments
    attr.comments['all'] = [Comment(t._val) for t in body if isinstance(t, tok.Comment)]

    parts = tok.split(body, tok.Pipe, include_separators=False)

    # Deal with ids first

    # Filter out any non-identifiers
    # FIXME: Need to check for unexpected tokens and report an error!
    part_1 = filter(lambda t: isinstance(t, tok.Identifier), parts[0])  # type: ignore

    # Convert them into References
    attr._data['ids'] = [Ref(str(id), 'LexicalUnit') for id in part_1]

    # Now we deal with lemmas
    if len(parts) >= 2:
        part_2 = filter(lambda t: isinstance(t, tok.Word), parts[1])  # type: ignore
        attr._data['lemmas'] = [str(lem) for lem in part_2]

    return attr


@AttributeFactory.register_parser('synon')
def parse_synon(head, body) -> Attrib:
    """
        Parses the synon attribute.

        The body of the synon attribute consists of semicolon separated groups of synonymous
        words (possibly different for each aspect, specified by prefixing the aspect name
        followed by a colon), each group is a comma separated list of words (or multiple words
        separated by spaces), e.g.::

            -synon: impf: přemisťovat, vodit; příp. vybírat
                    pf: přemístit, přivést; zavést; příp. vybrat

        This would be parsed into the following dict::

            {
                'impf:[
                    ['přemisťovat', 'vodit'],
                    ['příp. vybírat']
                ],
                'pf':[
                    ['přemístit', 'přivést'],
                    ['zavést'],
                    ['příp. vybrat']
                ]
            }

        Returns:
            The parsed attribute whose :attr:`_data <.data_structures.attribs.Attrib._data>` is a dictionary
            keyed by the aspect whose values are the synonym groups, each being a list of
            (multi)word synonyms.
    """
    attr = Attrib(str(head))
    attr._data = {}

    parsed_data, attr.comments = parse_keyval(body)

    # Make a dictionary keyed by vid, values are lists of synonym groups (separated by semicolons)
    data = {k: tok.split(v, tok.Semicolon, include_separators=False) for k, v in parsed_data.items()}  # type: ignore

    # Convert each synonym group into a list of multi words (separated by commas);
    # Moreover, convert each multi word (a list of tokens) into a string using tok.join
    attr._data = {
        k: [
            [
                tok.join(multi_word, '').strip() for multi_word in tok.split(syn_grp, tok.Comma, include_separators=False)  # type: ignore
            ] for syn_grp in groups
        ] for k, groups in data.items()
    }
    return attr
