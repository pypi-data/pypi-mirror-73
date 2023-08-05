""" Provides the Location class used to track source locations.
"""
from typing import List, Optional
from .json_utils import register as json_register


@json_register
class Location:
    """ Represents a location in a source of text.

        Provides functions to keep track of the (line, column) numbers (as well as the
        character-based index) and a method to pretty print the location with a selected
        number of lines of context.

        Attributes:

            _src:   the source text
            _fname: the (optional) filename from which source was read
    """

    @classmethod
    def location_from_pos(cls, src: str, pos: int, filename: Optional[str] = ''):
        """
            Creates a location from the 0-based character index `pos` in `src`.
        """
        loc = Location(src, filename=filename, ln=0, col=0, pos=0)
        for char in src:
            loc._inc_pos()
            if char == '\n':
                loc._newline()
            if loc.pos >= pos:
                break
        return loc

    __slots__ = '_src', '_fname', '_ln', '_col', '_pos'

    def __init__(self, src: str = '', filename: Optional[str] = '', ln: int = 0, col: int = 0, pos: int = 0):
        self._src = src
        self._fname = filename
        self._ln = ln
        self._col = col
        self._pos = pos

    @property
    def line(self):
        """The 0-based line number."""
        return self._ln

    @property
    def column(self):
        """The 0-based column number."""
        return self._col

    @property
    def pos(self):
        """The 0-based character index."""
        return self._pos

    def _inc_pos(self, delta=1):
        self._pos += delta
        self._col += delta

    def _newline(self):
        self._ln += 1
        self._col = 0

    def clone(self):
        """Creates a copy of the current location."""
        return Location(self._src, filename=self._fname, ln=self._ln, col=self._col, pos=self._pos)

    def context(self, num_ctx_lines: int = 4) -> List[str]:
        """A function to create a list of lines surrounding the position given by the Location.

           Returns:

                A list of strings, each string either empty (context-lines are separated from the current line
                by an empty string) or representing a line of source, each line preceded by its line number.
                For example, if `num_ctx_lines` is ``3``, and assuming current position is on line 4, column 3
                the following list might be returned::

                    [
                      '1  import json',
                      '2',
                      '3  a = json.dumps({'a': 10})',
                      '',
                      '4  b = 20',
                      '      ^',
                      '5  c = 10',
                      '6  print(b, c, a)',
                      '7  exit(1)'
                    ]

                This can then be printed out using, e.g. (``print('\\n'.join(loc.context(3)))``).
        """
        ln = self.line
        col = self.column

        # Get the Context
        src_lines = self._src.split('\n')

        # If there is just a single line, don't bother with line numbers and context lines
        if len(src_lines) < 2:
            return ["src: "+self._src, "     "+" "*col+"^"]

        start_ctx = max(ln-num_ctx_lines, 0)
        end_ctx = min(ln+num_ctx_lines+1, len(src_lines))
        prev_lines = src_lines[start_ctx:ln]
        post_lines = src_lines[ln+1:end_ctx]

        # Get the current line with a caret indicating the column
        cur_lines = ['', src_lines[ln], " "*col+"^"]

        # Prepend line numbers & current line marker
        line_num_len = len(str(end_ctx))
        for i in range(len(prev_lines)):
            prev_lines[i] = '  '+str(start_ctx+i).ljust(line_num_len+2) + prev_lines[i]

        cur_lines[1] = '> ' + str(ln).ljust(line_num_len) + cur_lines[1]
        cur_lines[2] = '  ' + ''.ljust(line_num_len) + cur_lines[2]

        for i in range(len(post_lines)):
            post_lines[i] = '  ' + str(ln+i).ljust(line_num_len+2) + post_lines[i]

        return prev_lines + cur_lines + post_lines

    def __str__(self):
        ret = ''
        if self._fname is not None:
            ret += self._fname+": "
        ret += '{ln}, {col}'.format(ln=self.line, col=self.column)
        return ret

    def __repr__(self):
        return str(self)

    def __json__(self, **opts):
        return {'ln': self._ln, 'col': self._col, 'pos': self._pos, 'fname': self._fname}

    @classmethod
    def from_json(cls, dct):
        """
            Constructs a location from a simple dict.
        """
        return cls(src='', filename=dct['fname'], ln=dct['ln'], col=dct['col'], pos=dct['pos'])
