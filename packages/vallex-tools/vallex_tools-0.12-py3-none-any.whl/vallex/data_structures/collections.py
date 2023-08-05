""" This file contains definitions of Lexicons and Lexicon collections.





    This module contains two classes:

    - :class:`Lexicon` represents a collection of lexemes
    - :class:`LexiconCollection` represents a collection of lexicons.

    which are used to represent collections of vallex data. Instances of these
    classes are what one gets when loading data from a file. Typically, a file
    will correspond to a lexicon. However, most functions working on the dataset
    take a LexiconCollection argument so one uses a LexiconCollection even
    when it contains just a single lexicon::

        from vallex import load_lexicon, LexiconCollection

        collection = LexiconCollection()
        lexicon = load_lexicon(open('v-vallex.txt','r', encoding='utf-8'))

        collection.add_lexicon(lexicon)

    The ``txt`` format allows only a single lexicon per file. However the ``JSON`` format
    also allows storing lexicon collections. Calling :func:`vallex.load_lexicon` on
    a file containing a lexicon collection would lead to an error. This is solved
    by using the :func:`vallex.add_file_to_collection` function::

        from vallex import add_file_to_collection, LexiconCollection

        collection = LexiconCollection()
        add_file_to_collection(collection, open('lexicon_or_lexicon_collection.json','r', encoding='utf-8'))

    which knows how to deal with both lexicons and lexicon collections.
"""
import datetime
import hashlib
import os

from typing import Dict, Iterable, List, Optional, Tuple

from ..json_utils import dump, register as json_register

from .lexical_unit import Lexeme, LexicalUnit
from .utils import Comment


@json_register
class Lexicon:
    """
        A class representing a collection of lexemes loaded from a single file.

        Attributes:
            _preamble: holds comments pertaining to the whole lexicon
                       (i.e. the comments which, in the ``txt`` format, come before
                       any lexemes)
    """

    def __init__(self, lexemes: Optional[Iterable[Lexeme]] = None, preamble: Optional[Iterable[Comment]] = None, path: str = ''):
        self._lexemes = lexemes or []
        self._preamble = preamble or []
        self._path = path
        self._checksum: Optional[str] = None
        self._errors: List[Tuple[str, str]] = []

    @property
    def lexemes(self) -> Iterable[Lexeme]:
        """
            An iterator iterating over all lexemes in the collection
        """
        return self._lexemes

    @property
    def lexical_units(self) -> Iterable[LexicalUnit]:
        """
            An iterator iterating over all lexical units in the collection
        """
        for lex in self.lexemes:
            for lu in lex.lexical_units:
                yield lu

    @property
    def path(self):
        """
            The path to the file from which the collection was loaded.

            It is used by :meth:`LexiconCollection.id2lexicon` as an id
            of the lexicon.
        """
        return self._path

    @path.setter
    def path(self, val):
        self._path = val

    def write_to_disk(self, backup: bool = False):
        """
            Saves the collection to the file it was originally loaded from.


            Arguments:
                backup: If true, the collection is not saved to the original
                        path but a ``.backup`` suffix is added to the path first.

            Note:
                If the lexicon was loaded from a ``txt`` formatted file, this function
                works by writing out the ``source`` of each lexeme to the file. In
                particular, it only saves changes which are reflected in the lexeme
                source. So, e.g., the following would not work::

                    # Load a lexicon
                    lexicon = load_lexicon(open('v-vallex.txt','r', encoding='utf-8'))

                    # Change all lexical ids by prefixing them with 'new-prefix'
                    for lu in lexicon.lexical_units:
                        lu._id = 'new-prefix-'+lu._id

                    # Save the changes back
                    # (!! DOES NOT WORK !!)
                    lexicon.write_to_disk()


                To be able to save data modified in this way, look at how the ``grep`` or ``transform``
                commands in :mod:`vallex.cli` are implemented. This function is used by
                the web interface to save changes when a user modifies the **source** of a lexical unit.
                FIXME: We should provide a standard way to do it instead of pointing people to look into :mod:`vallex.cli`.
        """
        check = hashlib.sha512()
        if backup:
            fname = self._path+'.backup'
        else:
            fname = self._path
        with open(fname, 'w', encoding='utf-8') as OUT:
            if self._path.endswith('json'):
                dump(self, OUT)
                # FIXME: we should update the checksum
                self._checksum = None
                return

            def wrln(*args):
                str_arg = ' '.join([str(a) for a in args])+"\n"
                check.update(bytes(str_arg, encoding='utf-8'))
                OUT.write(str_arg)

            wrln("# START ==========", self._path, "========== START")
            wrln("# Saved on:", datetime.datetime.today())
            wrln("#")
            for comment in self._preamble:
                wrln("#", comment)
            for lex in self.lexemes:
                wrln("*", lex._id)
                for comment in lex.comments:
                    wrln(" #", comment)
                for lu in lex.lexical_units:
                    wrln(' '+lu.src.strip())
                    wrln()
        self._checksum = check.hexdigest()

    def checksum(self):
        """
            Returns a checksum of the source file.

            For efficiency reasons the checksum is only computed when loading (or saving)
            the file. Afterwards it is cached and the cached value is returned.
        """
        if not self._checksum:
            self._checksum = self._on_disk_checksum()
        return self._checksum

    def _on_disk_checksum(self):
        with open(self._path, 'rb') as IN:
            return hashlib.sha512(IN.read()).hexdigest()

    def changed_on_disk(self, since: float):
        """
            Tests whether the source file has changed since `since`.

            Arguments:
                since: the time (as returned by os.stat.st_mtime) specified in seconds
                       of the Unix epoch.

            Whether a file has changed is determined by first looking at the
            ``m_time`` attribute of the file and, if it is more recent than `since`,
            its checksum is computed and compared to the checksum stored in memory.
        """
        if not os.path.exists(self._path):
            return True
        if os.stat(self._path).st_mtime < since:
            return False
        if not self._checksum:
            return False
        return self._checksum != self._on_disk_checksum()

    def __str__(self):
        return "Lexicon("+self.path+")"

    def __len__(self):
        """
            Returns the total number of lexical units stored in the collection.
        """
        return sum([len(lex) for lex in self.lexemes])

    def __json__(self, **opts):
        return {'path': self._path, 'preamble': list(self._preamble), 'lexemes': list(self._lexemes)}

    @classmethod
    def from_json(cls, dct):
        """
            Constructs a lexicon from a simple dict.
        """
        return Lexicon(dct.get('lexemes', []), dct.get('preamble', []), dct.get('path', ''))


@json_register
class LexiconCollection:
    """
        A class representing a collection of lexicons coming from different files.
    """

    def __init__(self, lexicons: Optional[Iterable[Lexicon]] = None):
        self._lexicons: Dict[str, Lexicon] = {}
        if lexicons:
            self._lexicons = {lexicon._path: lexicon for lexicon in lexicons}
        self._lexemes = {lex._id: lex for lex in self.lexemes}
        self._lexical_units = {lu._id: lu for lu in sum([lex.lexical_units for lex in self._lexemes.values()], [])}
        self._errors: List[Tuple[str, str]] = []

    def __len__(self):
        """
            Returns the total number of lexical units stored in the collection.
        """
        return len(self._lexical_units)

    @property
    def lexemes(self) -> Iterable[Lexeme]:
        """
            This property is an iterator over all lexemes stored in the collection.
        """
        for lexicon in self.lexicons:
            for lex in lexicon.lexemes:
                yield lex

    @property
    def lexical_units(self) -> Iterable[LexicalUnit]:
        """
            This property is an iterator over all lexical units stored in the collection.
        """
        return self._lexical_units.values()

    @property
    def lexicons(self) -> Iterable[Lexicon]:
        """
            This property is an iterator over all lexicons in the collection
        """
        return self._lexicons.values()

    @property
    def lexicon_paths(self) -> Iterable[str]:
        """
            This property is an iterator over the source paths of all lexicons stored
            in the collection.
        """

        return [lexicon._path for lexicon in self.lexicons]

    def id2lu(self, lu_id: str) -> LexicalUnit:
        """
            Returns the lexical unit with id `lu_id`.


            Raises:
                KeyError: If a lexical unit with the id given does not exist.
        """
        return self._lexical_units[lu_id]

    def id2lex(self, lex_id: str) -> Lexeme:
        """
            Returns the lexical unit with id `lex_id`.

            Raises:
                KeyError: If a lexeme with the id given does not exist.
        """

        return self._lexemes[lex_id]

    def id2lexicon(self, lexicon_path: str) -> Lexicon:
        """
            Returns the lexicon whose source path is `lexicon_path`.

            Raises:
                KeyError: If a lexicon with the given path does not exist.
        """
        return self._lexicons[lexicon_path]

    def lexeme_count(self) -> int:
        """
            Returns the total number of lexemes stored in the collection.
        """
        return sum([len(lexicon) for lexicon in self.lexicons])

    def __json__(self, **opts):
        return {'lexicons': list(self.lexicons)}

    @classmethod
    def from_json(cls, dct):
        """
            Constructs a lexicon collection from a simple dict.
        """
        return LexiconCollection(dct.get('lexicons', []))

    def extend(self, coll: 'LexiconCollection'):
        """
            Adds all the lexicons in collection `coll` to the current collection.
        """
        for lexicon in coll.lexicons:
            self.add_lexicon(lexicon)

    def add_lexicon(self, lexicon: Lexicon):
        """
            Adds the lexicon `lexicon` to the current collection.
        """
        self.update_lexicon(lexicon)

    def update_lexicon(self, lexicon: Lexicon):
        """
            Updates the lexicon `lexicon` in the current collection.

            Note:
                - If the lexicon is not already in the collection, it is added first.
                - The update only updates data for the lexemes and lexical units which are in the
                  provided lexicon. In particular, if a lexeme or lexical unit is deleted from a lexicon
                  and :meth:`update_lexicon` is called on it, this
                  will not be reflected in the current collection (if, e.g., a lexical unit is deleted,
                  it will stay in the current collection; if its parent lexeme is not deleted at the
                  same time, it will be updated so it won't contain the deleted unit leading to inconsistent
                  state -> the deleted unit will be accessible through the :meth:`lexical_units` property
                  but not through its parent lexeme).
        """
        self._lexicons[lexicon._path] = lexicon
        self._lexemes.update({lex._id: lex for lex in lexicon.lexemes})
        self._lexical_units.update({lu._id: lu for lu in sum([lex.lexical_units for lex in lexicon.lexemes], [])})

    def remove_lexicon(self, lexicon: Lexicon):
        """
            Removes the lexicon `lexicon` from the current collection.
        """
        del self._lexicons[lexicon._path]
        for lex in lexicon.lexemes:
            del self._lexemes[lex._id]
        for lu in lexicon.lexical_units:
            del self._lexical_units[lu._id]

    def update_lu(self, old_lu: Optional[LexicalUnit], new_lu: LexicalUnit):
        """
            Updates the lexical unit `old_lu` in the current collection with data from
            the new lexical unit `new_lu`. If `old_lu` is None, the new_lu is just
            added to the collection.

            Note: The new_lu must have a parent which already exists in the collection
            (i.e. this method can't create new lexemes!)
        """
        self._lexical_units[new_lu._id] = new_lu
        if old_lu:
            ids = [lu._id for lu in old_lu._parent.lexical_units]  # type: ignore
            old_lu._parent.lexical_units = [self._lexical_units[id] for id in ids]  # type: ignore
        else:
            new_lu._parent.lexical_units.append(new_lu)  # type: ignore
