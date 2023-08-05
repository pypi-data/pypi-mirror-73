""" Implements some high level helpers



    This module implements helpers for loading lexicon data from files.
"""
import sys

from pathlib import Path
from typing import IO, Optional, Union

from .config import Config
from .data_structures import LexiconCollection, Lexicon
from .error import UnknownFormat
from .json_utils import load
from .term import ProgressCallback
from .txt_parser import parse_token_stream
from .txt_tokenizer import TokenStream


def load_file(src: IO, fmt: Optional[str] = None, progress_cb: Optional[ProgressCallback] = None) -> Union[Lexicon, LexiconCollection]:
    """
        Loads either a lexicon or a lexicon collection from a file.

        Arguments:
            src:    the file to load
            fmt:    optionally specifies the format of the file and should be
                    either 'json' or 'txt'; if not specified the format
                    is guessed from `src.name`: if it ends with 'json',
                    it is assumed the format is JSON, otherwise textual
                    format is expected

        Raises:
            UnknownFormat: This exception is raised in either of the following
                           scenarios:

                           1. fmt is specified and is not ``txt`` or ``json``
                           2. the format is specified or guessed to be JSON, but
                              the loaded data does not have type :class:`Lexicon <.data_structures.collections.Lexicon>`
                              or :class:`Lexicon <.data_structures.collections.LexiconCollection>`
        Note:
            The textual format can't store lexicon collections.
    """
    if not fmt:
        if src.name.endswith('json'):
            fmt = 'json'
        else:
            fmt = 'txt'
    elif fmt not in ['json', 'txt']:
        raise UnknownFormat("Unknown format: "+fmt+" (supported formats: json, txt)")

    if fmt == 'json':
        return load(src)

    src_content = src.read()
    total_size = len(src_content)
    stream = TokenStream(src_content, fname=src.name)
    if progress_cb:
        def callback(pos, lexeme_count):
            progress_cb(pos/total_size, "("+str(lexeme_count) + " lexemes)")
        lexicon = parse_token_stream(stream, callback)
    else:
        lexicon = parse_token_stream(stream)
    lexicon.path = src.name
    return lexicon


def load_lexicon(src: IO, fmt: Optional[str] = None, progress_cb: Optional[ProgressCallback] = None) -> Lexicon:
    """
        Loads a lexicon from a file.

         Arguments:
            src:    the file to load
            fmt:    optionally specifies the format of the file and should be
                    either 'json' or 'txt'; if not specified the format
                    is guessed from `src.name`: if it ends with 'json',
                    it is assumed the format is JSON, otherwise textual
                    format is expected
         Raises:
            UnknownFormat: This exception is raised in either of the following
                           scenarios:

                           1. fmt is specified and is not ``txt`` or ``json``
                           2. the format is specified or guessed to be JSON, but
                              the loaded data does not have type :class:`Lexicon <.data_structures.collections.Lexicon>`
    """
    data = load_file(src, fmt, progress_cb=progress_cb)

    if isinstance(data, Lexicon):
        return data

    raise UnknownFormat("Invalid input file: "+src.name+" (expected Lexicon got "+str(type(data))+" instead).")


def add_file_to_collection(coll: LexiconCollection, src: IO, fmt: Optional[str] = None, progress_cb: Optional[ProgressCallback] = None):
    """
        Loads a lexicon or lexicon collection from a file and all the lexicons to `coll`.

         Arguments:
            coll:           the collection to add the lexicons to
            src:            the file to load
            fmt:            optionally specifies the format of the file and should be
                            either 'json' or 'txt'; if not specified the format
                            is guessed from `src.name`: if it ends with 'json',
                            it is assumed the format is JSON, otherwise textual
                            format is expected
            progress_cb:    Called periodically during loading to indicate progress (e.g. for outputting a progressbar)

         Raises:
            UnknownFormat: This exception is raised in either of the following
                           scenarios:

                           1. fmt is specified and is not ``txt`` or ``json``
                           2. the format is specified or guessed to be JSON, but
                              the loaded data does not have type :class:`Lexicon <.data_structures.collections.Lexicon>`
                              or :class:`Lexicon <.data_structures.collections.LexiconCollection>`
         Note:
            The textual format can't store lexicon collections.
    """
    lex_or_coll = load_file(src, fmt=fmt, progress_cb=progress_cb)
    if isinstance(lex_or_coll, LexiconCollection):
        coll.extend(lex_or_coll)
    elif isinstance(lex_or_coll, Lexicon):
        coll.add_lexicon(lex_or_coll)
    else:
        raise UnknownFormat("Invalid input file: "+src.name+" (expected Lexicon or LexiconCollection got "+str(type(lex_or_coll))+" instead).")


def add_path_to_collection(coll: LexiconCollection, config: Config, path: Union[Path, str], fmt: Optional[str] = None, progress_cb: Optional[ProgressCallback] = None):
    """
        Loads a lexicon or lexicon collection from a file and all the lexicons to `coll`.

        Like :func:`add_file_to_collection` except that the file is not specified as an input stream but as
        a path (a string or a Path object). Additionally, if the path is not absolute, the lexicon directories
        (determined from the `config` object searched to find it.

         Arguments:
            coll:           the collection to add the lexicons to
            config:         a configuration object which is used to get information where to search for the lexicon
            path:           the file to load
            fmt:            optionally specifies the format of the file and should be
                            either 'json' or 'txt'; if not specified the format
                            is guessed from `src.name`: if it ends with 'json',
                            it is assumed the format is JSON, otherwise textual
                            format is expected
            progress_cb:    Called periodically during loading to indicate progress (e.g. for outputting a progressbar)

         Raises:
            FileNotFoundError: This exception is raised if the path is not found

            All exceptions raised by :func:`add_file_to_collection`.
    """
    p = config.resolve_lex_path(Path(path))
    if not p:
        raise FileNotFoundError
    with p.open('r', encoding='utf-8') as IN:
        add_file_to_collection(coll, IN, fmt=fmt, progress_cb=progress_cb)


if sys.version_info[1] < 5:
    from importlib.machinery import SourceFileLoader

    def _import_python_file(parent_module: str, path: Path):
        return SourceFileLoader(parent_module+'.'+path.stem, str(path.absolute())).load_module(parent_module+'.'+path.stem)
else:
    import importlib.util

    def _import_python_file(parent_module: str, path: Path):
        spec = importlib.util.spec_from_file_location(parent_module+'.'+path.stem, str(path.absolute()))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)  # type: ignore
        return mod
