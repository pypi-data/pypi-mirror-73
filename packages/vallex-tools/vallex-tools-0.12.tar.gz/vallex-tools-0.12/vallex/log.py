"""
    This module configures logging.





    The module, by default, sets a console handler which logs all messages
    with log-level above and including INFO to the console. The handler has
    a colored formatter (:class:`ColoredFormatter`) which uses
    :func:`format_text <vallex.term.format_text>` to make the logs look nice and colourful. The
    log-level treshold can be modified by the ``--verbosity`` flag on the
    command line (see :mod:`main <vallex.main>`).

    The module also provides the function :func:`load_config` which sets-up
    logging to a file based on configuration present in a :class:`Config <vallex.config.Config>`
    object.

    Finally, the module sets up an except hook :func:`exception_hook` to handle uncaught
    exceptions and log them and a convenience function :func:`log_wsgi_request` to
    log web-server requests.
"""
import copy
import io
import logging
import os
import re
import sys
import traceback

from .term import FG, Color, RED, YELLOW, WHITE, GRAY, IOMode, format_text, IOMode
from .config import Config

from vallex.vendor import better_exceptions


class ColoredFormatter(logging.Formatter):
    """
        A log formatter which uses :func:`format_text <vallex.term.format_text>`
        to nicely format & color log messages destined for the console.
    """
    COLOR_MAPPING = {
        'DEBUG':        Color(fg=GRAY, mode=IOMode.TERM),
        'INFO':         Color(fg=WHITE, mode=IOMode.TERM),
        'WARNING':      Color(fg=YELLOW, mode=IOMode.TERM),
        'ERROR':        Color(fg=RED, mode=IOMode.TERM),
        'CRITICAL':     Color(fg=WHITE, bg=RED, mode=IOMode.TERM),
    }

    def format(self, record):
        colored_record = copy.copy(record)
        color = self.COLOR_MAPPING.get(record.levelname, Color(fg=WHITE, mode=IOMode.TERM))
        colored_record.levelname = color | record.levelname
        colored_record.filename = Color(fg=GRAY, mode=IOMode.TERM) | record.filename
        colored_record.msg = format_text(record.msg, mode=IOMode.TERM)
        return super().format(colored_record)


class PlainFormatter(logging.Formatter):
    """
        A log formatter which uses :func:`term.format_text <vallex.term.format_text>`
        to format log messages destined to a file (or other place which can't handle
        ansi escape sequences-based formatting)
    """

    def format(self, record):
        colored_record = copy.copy(record)
        colored_record.msg = format_text(record.msg, mode=IOMode.PLAIN)
        return super().format(colored_record)


_LOG_FORMATTER = ColoredFormatter("[%(name)s][%(levelname)s]  %(message)s (%(filename)s:%(lineno)d)")
_CONSOLE_HANDLER = logging.StreamHandler()
_CONSOLE_HANDLER.setFormatter(_LOG_FORMATTER)
_CONSOLE_HANDLER.setLevel(logging.INFO)

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
root_logger.addHandler(_CONSOLE_HANDLER)


_LOGGING_SRCFILE = os.path.normcase(logging.addLevelName.__code__.co_filename)
_THIS_SRCFILE = __file__


def load_config(cfg: Config):
    """
        Sets up logging as specified in the configuration.
    """

    default_level = getattr(logging, cfg.default_log_level.upper(), logging.INFO)
    component_res = [(re.compile(c.replace('*', '.*'), re.IGNORECASE), getattr(logging, l.upper(), 'INFO')) for c, l in cfg.log_filters.items()]

    def should_log(record):
        for c_re, l in component_res:
            if c_re.match(record.name.replace(':', '.')):
                return record.levelno >= l
        return record.levelno >= default_level

    try:
        _FILE_HANDLER = logging.FileHandler(cfg.log_file, encoding='utf-8')
        _FILE_HANDLER.setFormatter(PlainFormatter("%(asctime)s [%(name)s][%(levelname)s]  %(message)s (%(filename)s:%(lineno)d)"))
        _FILE_HANDLER.addFilter(should_log)
        _FILE_HANDLER.setLevel(logging.DEBUG)
        root_logger.addHandler(_FILE_HANDLER)
    except Exception as ex:
        log("log", logging.DEBUG, "Error setting up log handler", "".join(exc_formatter.format_exception(*sys.exc_info())))
        log("log", logging.ERROR, "Could not log to", FG(YELLOW) | cfg.log_file, "error:", FG(RED) | ex)


def find_caller(self, stack_info=False):
    """
        Find the stack frame of the caller so that we can note the source
        file name, line number and function name.

        This function comes straight from the original python one
    """
    frame = sys._getframe(4)
    # On some versions of IronPython, currentframe() returns None if
    # IronPython isn't run with -X:Frames.
    if frame is not None:
        frame = frame.f_back
    ret = "(unknown file)", 0, "(unknown function)", ""
    while hasattr(frame, "f_code"):
        code_obj = frame.f_code
        filename = os.path.normcase(code_obj.co_filename)
        if filename in [_LOGGING_SRCFILE, _THIS_SRCFILE] or 'error.py' in filename:
            frame = frame.f_back
            continue
        sinfo = None
        if stack_info:
            sio = io.StringIO()
            sio.write('Stack (most recent call last):\n')
            traceback.print_stack(frame, file=sio)
            sinfo = sio.getvalue()
            if sinfo[-1] == '\n':
                sinfo = sinfo[:-1]
            sio.close()
        ret = (code_obj.co_filename, frame.f_lineno, code_obj.co_name, sinfo)
        break
    return ret


def log(component, level, *msg):
    """
        A helper function to use the logging module to output a log message.
    """
    logger = logging.getLogger(component)
    logger.findCaller = find_caller
    logger.log(level, ' '.join([str(m) for m in msg]))


exc_formatter = better_exceptions.ExceptionFormatter(
    colorize=False,
    diagnose=True,
    encoding='utf-8',
    backtrace=True
)


def exception_hook(exc, value, tb):
    """
        A hook to pretty print uncaught exceptions and forward them
        to the log.
    """
    lines = "".join(exc_formatter.format_exception(exc, value, tb))
    log("system", logging.CRITICAL, lines)


sys.excepthook = exception_hook


def log_wsgi_request(handler_self, code='-', size='-'):
    """
        A helper function used by the WSGIServer (in bottle.py)
        to nicely (colourfully) log http requests using the log
        function.
    """
    if hasattr(code, 'value'):
        code = code.value
    code = str(code)
    if code.startswith('4'):
        code = "<red>" + str(code) + "</red>"
    elif code.startswith('2'):
        code = "<green>" + str(code) + "</green>"
    else:
        code = "<yellow>" + str(code) + "</yellow>"
    words = handler_self.requestline.split()
    if len(words) == 3:
        command, path, version = words
        requestline = command+' <b>'+path+'</b> '+'<gray>'+version+'</gray>'
    elif len(words) == 2:
        command, path = words
        requestline = command+' <b>'+path+'</b> '
    else:
        requestline = '<red>'+handler_self.requestline+'</red>'

    log('bottle:wsgi_server', logging.DEBUG, requestline, code, size)
