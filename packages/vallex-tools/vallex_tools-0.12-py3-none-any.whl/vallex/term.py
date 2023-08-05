"""
    Provides helper functions for terminal output.

    Includes termsize.py (plumbum.cli.termsize)
    taken from Plumbum (https://plumbum.readthedocs.io/en/latest/index.html).
"""

from __future__ import division, print_function, absolute_import

import enum
import os
import platform
import re
import sys
try:
    import termios
    import tty
except:
    pass

from struct import Struct
from typing import Callable, Optional


# See, e.g.,  https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences
_CLEAR_SCREEN_SEQ = '\033[2J\033[1;1H'
_BOLD_CODE = 1
_DIM_CODE = 2
_ITALIC_CODE = 3
_UNDERLINE_CODE = 4
_BLINK_CODE = 25
_REVERSE_CODE = 7
_HIDDEN_CODE = 8
_STRIKEOUT_CODE = 9


class IOMode(enum.IntEnum):
    """
        The components of a semver triple.
    """
    TERM = 0
    PLAIN = 1
    QT = 2


MODE = IOMode.TERM


class Color:
    """
       Inspired by plumbum.colorlib. A helper class for formatting text using ansi escape sequences.

       Each instance of the class corresponds to a formatting style: a combindation of foreground/background
       color and font style (bold,underline,italic). To apply the style to a string, use the pipe
       operator

       .. code-block:: python

          print(Color(bold=True) | "This text will be in bold")
          print(Color(italic=True) | "And this will be italic")

       which wraps its right argument with the correct ansi sequences (in case the mode is set to TERM,
       if its set to QT, it wraps it in html tags, if set to plain, it returns the string as is)
    """
    _RESET_FG = 39
    _RESET_BG = 49
    _RESET_BOTH = 0
    _RESET_BOLD = 22
    _RESET_UNDERLINE = 24
    _RESET_ITALIC = 23
    _RESET_ALL = 0

    def __init__(self, fg=None, bg=None, bold=False, underline=False, italic=False, mode=None):
        self.fg = fg
        self.bg = bg
        self.bold = bold
        self.underline = underline
        self.italic = italic
        self._mode = MODE if mode is None else mode

    @property
    def ansi_sequence(self):
        """This is the ansi sequence as a string, ready to use."""
        if self._mode == IOMode.TERM:
            return '\033[' + ';'.join(map(str, self.ansi_codes)) + 'm'
        if self._mode == IOMode.QT:
            style = ''
            if self.bg:
                style += 'background-color: rgb('+','.join([str(c) for c in self.bg])+');'
            if self.fg:
                style += 'color: rgb('+','.join([str(c) for c in self.fg])+');'
            ret = """<span style='{style}'>""".format(style=style)
            if self.underline:
                ret += '<u>'
            if self.italic:
                ret += '<i>'
            if self.bold:
                ret += '<b>'
            return ret
        return ""

    @property
    def ansi_codes(self):
        """This is the ANSI reset sequence for the full style (color, bold, ...)."""
        codes = []
        if self.fg:
            codes.extend([38, 2, self.fg[0], self.fg[1], self.fg[2]])
        if self.bg:
            codes.extend([48, 2, self.bg[0], self.bg[1], self.bg[2]])
        if self.bold:
            codes.append(_BOLD_CODE)
        if self.underline:
            codes.append(_UNDERLINE_CODE)
        if self.italic:
            codes.append(_ITALIC_CODE)
        return codes

    @property
    def reset(self):
        """
            Returns the ANSI sequence to reset the terminal back to normal
            as a string, ready to use.
        """
        if self._mode == IOMode.TERM:
            codes = []
            if self.fg:
                codes.append(self._RESET_FG)
            if self.bg:
                codes.append(self._RESET_BG)
            if self.bold:
                codes.append(self._RESET_BOLD)
            if self.underline:
                codes.append(self._RESET_UNDERLINE)
            if self.italic:
                codes.append(self._RESET_ITALIC)
            return '\033['+';'.join(map(str, codes)) + 'm'
        if self._mode == IOMode.QT:
            ret = ''
            if self.bold:
                ret += '</b>'
            if self.italic:
                ret += '</i>'
            if self.underline:
                ret += '</u>'
            return ret + '</span>'
        return ""

    def wrap(self, text):
        """
            Wraps text so that the result contains an ANSI sequence to set
            the color followed by text and followed by an ANSI sequence to
            reset the color.
        """
        return self.ansi_sequence + str(text) + self.reset

    def __getitem__(self, key):
        return self.wrap(key)

    def __or__(self, other):
        return self.wrap(other)


def FG(col, mode=None):
    """
        A shortcut to create an instance of the Color class with
        foreground set to `col`.
    """
    return Color(fg=col, mode=mode)


def BG(col, mode=None):
    """
        A shortcut to create an instance of the Color class with
        background set to `col`.
    """
    return Color(bg=col, mode=mode)


RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 170, 0)
BLUE = (0, 0, 170)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

COLOR_OK = FG(GREEN)
COLOR_ERROR = FG(RED)


def format_text(txt: str, mode: Optional[IOMode] = None) -> str:
    """
        Formats a Markdown/HTML-style formatted text for display.

        Arguments:
                txt:  The text to format
                mode: The output medium (e.g., terminal, plain, qt, ...), if
                      it is not specified, term.MODE is used

        The following markup is recognized

        - ``**text**``, ``<b>text</b>``   ... ``text`` is formatted in bold
        - ``*text*``, ``<i>text</i>``     ... ``text`` is formatted in italic
        - ``<u>text</u>``                 ... ``text`` is formatted underlined
        - ``<fg color>text</fg>``, ``<color>text</color>`` ... ``text`` is
                                                formatted in foreground color ``color``
        - ``<bg color>text</bg>``         ... ``text`` is formatted in background color ``color``

        where ``color`` can be any of ``red``, ``yellow``, ``green``, ``white``, ``gray``, ``blue``.
    """
    COLOR_MAP = {
        'RED': RED,
        'YELLOW': YELLOW,
        'GREEN': GREEN,
        'WHITE': WHITE,
        'GRAY': GRAY,
        'BLUE': BLUE
    }
    COL_RE = re.compile("<(?P<coltype>fg|bg)\s+(?P<col>[^>]*)>(?P<text>[^<]*)</(?P=coltype)>", re.IGNORECASE)
    COL2_RE = re.compile("<\s*(?P<color>red|yellow|green|blue|white|gray)\s*>(?P<text>[^<]*)</(?P=color)>", re.IGNORECASE)

    def col_repl(m):
        col = m.group('col').upper()
        col = COLOR_MAP.get(col, None)
        if m.group('coltype').upper() == 'FG':
            col = FG(col, mode=mode)
        else:
            col = BG(col, mode=mode)
        return col.wrap(m.group('text'))

    def col2_repl(m):
        col = m.group('color').upper()
        col = COLOR_MAP.get(col, None)
        col = FG(col, mode=mode)
        return col.wrap(m.group('text'))

    EM_RE = re.compile("\*(?P<text>[^*]*)\*(?!\*)")
    I_RE = re.compile("<i>(?P<text>[^<]*)</i>", re.IGNORECASE)

    def em_repl(m):
        return Color(italic=True, mode=mode).wrap(m.group('text'))

    STRONG_RE = re.compile("\*\*(?P<text>[^*]*)\*\*")
    B_RE = re.compile("<b>(?P<text>[^<]*)</b>", re.IGNORECASE)

    def strong_repl(m):
        return Color(bold=True, mode=mode).wrap(m.group('text'))

    #UNDERLINE_RE = re.compile("\*\*(?P<text>[^*]*)\*\*")
    U_RE = re.compile("<u>(?P<text>[^<]*)</u>", re.IGNORECASE)

    def underline_repl(m):
        return Color(underline=True, mode=mode).wrap(m.group('text'))

    CODE_RE = re.compile("`(?P<text>[^`]*)`")
    C_RE = re.compile("<code>(?P<text>[^<]*)</code>", re.IGNORECASE)

    def code_repl(m):
        return Color(underline=True, mode=mode).wrap(m.group('text'))

    subs = [
        (COL_RE, col_repl),
        (COL2_RE, col2_repl),
        (EM_RE, em_repl),
        (I_RE, em_repl),
        (STRONG_RE, strong_repl),
        (B_RE, strong_repl),
        #(UNDERLINE_RE, underline_repl),
        (U_RE, underline_repl),
        (CODE_RE, code_repl),
        (C_RE, code_repl)
    ]
    ret = txt
    for pat, repl in subs:
        ret = pat.sub(repl, ret)
    return ret


class Interpolator:
    """
        A helper class for interpolating colors from a start color
        to an end color.
    """

    def __init__(self, max_val, start_col, end_col):
        start_r, start_g, start_b = start_col
        end_r, end_g, end_b = end_col
        self._max_val = max_val
        self._delta = (end_r-start_r), (end_g-start_g), (end_b-start_b)
        self._start_color = start_col

    def col(self, val):
        """
            Returns the color corresponding to the value val in the
            interval.
        """
        start_r, start_g, start_b = self._start_color
        delta_r, delta_g, delta_b = self._delta
        coeff = val/self._max_val
        ret_r = int(start_r+coeff*delta_r)
        ret_g = int(start_g+coeff*delta_g)
        ret_b = int(start_b+coeff*delta_b)
        return (ret_r, ret_g, ret_b)


class AbstractStatusLine:

    def start_action(self, *heading):
        """
        Starts a new statusline, printing out heading followed by a semicolon and empty status.
        """

    def end_action(self, ok=True, message=None, preserve_status=False):
        """
        If no message is provided, the status is updated with a green ``OK`` if (`ok` is ``True``) or a
        red ``ERROR`` (if `ok` is ``False``). If a message is provided, the status is updated with this message
        instead. If preserve_status is True, the status is not updated (i.e. the last status update
        remains). Finally a new line is started.

        """

    def update(self, *args, finish=False, clip=True):
        """
            Updates the current status (i.e. deletes the old status and replaces it with the new status).
            Status is composed by joining the stringified arguments (similar to how print works)
        """

    def print(self, *args, sep=' '):
        """
        """


class StatusLine(AbstractStatusLine):
    """
        A class for creating & updating status lines (something like a progressbar, but with textual updates).
        A new status line is created by calling `start_action`, the status is updated by calling `update`
        (which has a signature similar to the print function) and the status is finished by calling `end_action`.
        A progressbar-like usage might be implemented as follows::

            from term import status
            status.start_action("Doing bar")
            for i in range(100):
                status.update(i,"% finished")
            status.end_action()

    """

    def __init__(self, OUT=sys.stderr):
        self._lead_text = ''
        self._last_len = 0
        self._width = get_terminal_size(default=(0, 0))[0]
        self._out = OUT
        self._tty = os.isatty(self._out.fileno())

    def start_action(self, *heading):
        """
        Starts a new statusline, printing out heading followed by a semicolon and empty status.
        """
        self._clear()
        self._lead_text = ' '.join([str(h) for h in heading])+':'
        self._last_len = 0
        self.update()

    def end_action(self, ok=True, message=None, preserve_status=False):
        """
        If no message is provided, the status is updated with a green ``OK`` if (`ok` is ``True``) or a
        red ``ERROR`` (if `ok` is ``False``). If a message is provided, the status is updated with this message
        instead. If preserve_status is True, the status is not updated (i.e. the last status update
        remains). Finally a new line is started.

        """
        if not preserve_status:
            mlen = 0
            if message:
                message = '('+message+') '
                mlen += len(message)
            else:
                message = ''
            if ok:
                mlen += len('OK')+len(COLOR_OK.reset)+5
                result_text = message + (COLOR_OK | 'OK')
            else:
                mlen += len('ERROR')+len(COLOR_ERROR.reset)+5
                result_text = message + (COLOR_ERROR | 'ERROR')
            mlen += len(self._lead_text+' ')
            indent = (self._width-10) - mlen
            if indent > 0:
                result_text = str(' '*indent) + result_text
            self.update(result_text, clip=False)
        self._last_len = 0
        print(file=self._out)
        self._out.flush()

    def update(self, *args, finish=False, clip=True):
        """
            Updates the current status (i.e. deletes the old status and replaces it with the new status).
            Status is composed by joining the stringified arguments (similar to how print works)
        """
        self._clear()
        if finish:
            end = '\n'
        else:
            end = ''
        out_str = ' '.join([str(x) for x in args]).strip('\n')
        self._last_len = len(self._lead_text+' '+out_str)
        if clip and self._last_len > self._width:
            out_str = out_str[:-(self._last_len-(self._width-3))]+'...'
            self._last_len = self._width
        print(self._lead_text, out_str, end=end, flush=True, file=self._out)

    def print(self, *args, sep=' '):
        print(*args, flush=True, file=self._out, sep=sep)

    def progress_bar(self, title, width=20):
        return ProgressBar(title, width, self)

    def _clear(self):
        if self._tty:
            print("\r", self._last_len * " ", "\r", end='', sep='', file=self._out)
        elif self._last_len > 0:
            print(file=self._out)


def get_char():
    """
        Reads a single character from stdin without echoing it.

        Implementation taken from https://stackoverflow.com/questions/510357/python-read-a-single-character-from-the-user
    """
    if platform.system() == 'Windows':  # pragma: no cover
        import msvcrt
        return msvcrt.getch()

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def get_terminal_size(default=(80, 25)):
    """
    Get width and height of console; works on linux, os x, windows and cygwin
    Adapted from https://gist.github.com/jtriley/1108174
    Originally from: http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python
    """
    current_os = platform.system()
    if current_os == 'Windows':  # pragma: no cover
        size = _get_terminal_size_windows()
        if not size:
            # needed for window's python in cygwin's xterm!
            size = _get_terminal_size_tput()
    else:
        size = _get_terminal_size_linux()

    if size is None:  # we'll assume the standard 80x25 if for any reason we don't know the terminal size
        size = default
    return size


def _get_terminal_size_windows():  # pragma: no cover
    try:
        from ctypes import windll, create_string_buffer  # type: ignore
        stderr_handle = -12
        handle = windll.kernel32.GetStdHandle(stderr_handle)
        csbi_struct = Struct("hhhhHhhhhhh")
        csbi = create_string_buffer(csbi_struct.size)
        res = windll.kernel32.GetConsoleScreenBufferInfo(handle, csbi)
        if res:
            _, _, _, _, _, left, top, right, bottom, _, _ = csbi_struct.unpack(
                csbi.raw)
            return right - left + 1, bottom - top + 1
        return None
    except Exception:
        return None


def _get_terminal_size_tput():  # pragma: no cover
    # get terminal width
    # src: http://stackoverflow.com/questions/263890/how-do-i-find-the-width-height-of-a-terminal-window
    try:
        tput = local['tput']
        cols = int(tput('cols'))
        rows = int(tput('lines'))
        return (cols, rows)
    except Exception:
        return None


def _ioctl_GWINSZ(fd):
    size = Struct("hh")
    try:
        import fcntl
        return size.unpack(fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
    except Exception:
        return None


def _get_terminal_size_linux():
    size = _ioctl_GWINSZ(0) or _ioctl_GWINSZ(1) or _ioctl_GWINSZ(2)
    if not size:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            size = _ioctl_GWINSZ(fd)
            os.close(fd)
        except Exception:
            pass
    if not size:
        try:
            size = (int(os.environ['LINES']), int(os.environ['COLUMNS']))
        except Exception:
            return None
    return size[1], size[0]


def _catchall(meth):
    def decorated(*args, **kwargs):
        try:
            return meth(*args, **kwargs)
        except Exception as ex:
            print("Got exception running", meth, args, kwargs, "EXCEPTION:", ex)
    return decorated


class MultiModeStatusLine:
    @_catchall
    def start_action(self, *args, **kwargs):
        self._impl.start_action(*args, **kwargs)

    @_catchall
    def end_action(self, *args, **kwargs):
        self._impl.end_action(*args, **kwargs)

    @_catchall
    def update(self, *args, **kwargs):
        self._impl.update(*args, **kwargs)

    @_catchall
    def print(self, *args, **kwargs):
        self._impl.print(*args, **kwargs)

    @_catchall
    def progress_bar(self, *args, **kwargs):
        return self._impl.progress_bar(*args, **kwargs)

    def set_impl(self, impl):
        self._impl = impl


_term_status_line = StatusLine()

STATUS = MultiModeStatusLine()
STATUS.set_impl(_term_status_line)


ProgressCallback = Callable[[float, str], None]


class ProgressBar:
    """
        Provides  simple progressbar which can be used, e.g. as follows::

            from term import ProgressBar

            progress = ProgressBar("Iterating:")
            for i in range(250):
                cnt = do_some_stuff(i)
                progress.update(i/250, " ("+str(cnt)+" processed)")
            progress.done()

    """

    def __init__(self, title, width=20, status_line=STATUS):
        self._title = title
        self._width = width
        self._status = status_line
        self._status.start_action(title)

    def update(self, fraction, message):
        """
            Updates the progressbar to a fraction of its total width given by `fraction`
            and also prints out the message at the end of the (full) bar.
        """
        if fraction >= 1:
            bar_len = self._width
        else:
            bar_len = int(fraction*self._width)
        rem_len = self._width-bar_len
        self._status.update(bar_len*"#"+rem_len*" ", message)

    def done(self, message: str = ''):
        """
            Finishes the job and proceeds to the next line.
        """
        if message:
            success = False
        else:
            message = 'OK'
            success = True
        self._status.end_action(ok=success, message=message, preserve_status=success)
