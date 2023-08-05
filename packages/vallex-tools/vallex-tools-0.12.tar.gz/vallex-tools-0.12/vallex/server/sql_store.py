""" SQL Store




    When running the web interface, the Vallex Data is kept in four locations:

    - in the memory of the server process
    - in the memory of the browser accessing the page
    - in a sql database used by the server process
    - the source of the data (in txt format)


    The reason for the sql database is so that the server may synchronize access to
    the data from different browser pages / different users (although multiuser
    functions are not currently envisioned), since the server may run multiple
    processes to handle multiple browser requests at a time.

    The reason for the separate source of data in txt format is that vallex users
    are used to editing the data primarily in this form and it is not seen as practical
    to have the sql database be the 'source of truth'.

    This module implements the class SQLStore which handles the database storage
    of Vallex data.
"""
import logging
import sqlite3

from contextlib import contextmanager, closing
from pathlib import Path
from time import time
from typing import Iterable, Optional, Union, ContextManager

from vallex.data_structures import Lexeme, Lexicon, LexicalUnit, LexiconCollection
from vallex.json_utils import loads, dumps
from vallex.log import log


class LUIdChanged(Exception):
    pass


class LUChanged(Exception):
    pass


class SQLStore:
    """
        A class for accessing a sqlite-backed data store storing
        lexical units, lexemes and lexicons.
    """
    SCHEMA_COLLECTIONS = """
        CREATE TABLE IF NOT EXISTS lexicons (
            path TEXT,          -- the path where the lexicon source is stored
            preamble TEXT,      -- a string containing a JSON representation of the lexicon preamble
            checksum TEXT,      -- the checksum of the lexicon source
            version REAL        -- the timestamp of the time the lexicon was read from source
        )
    """
    SCHEMA_LEXEMES = """
        CREATE TABLE IF NOT EXISTS lexemes (
            id TEXT,            -- the id of the lexeme
            lexicon TEXT,       -- the lexicon (identified by its path) to which the unit belongs
            comments TEXT,      -- a string containing a JSON representation of the lexeme comments
            src_start TEXT,     -- a string containing a JSON representation of a Location instance
            src_end TEXT        -- a string containing a JSON representation of a Location instance
        )
    """
    SCHEMA_LUS = """
        CREATE TABLE IF NOT EXISTS lexical_units (
            id TEXT,            -- the id of the lexical unit
            parent TEXT,        -- the parent lexeme
            lexicon TEXT,       -- the lexicon (identified by its path) to which the unit belongs
            json_rep TEXT,      -- a string containing the JSON representation of the lexical unit
            author TEXT,        -- the author of the last modification
            version REAL        -- timestamp of the last modification
        )
    """

    def __init__(self, path: Union[str, Path]):
        self._collection: LexiconCollection = LexiconCollection()
        self._last_refresh: float = time()
        self._path = Path(path)

        # Set the isolation level to None to avoid
        # python randomly starting transactions leading to locks on the db
        # see http://charlesleifer.com/blog/multi-threaded-sqlite-without-the-operationalerrors/
        # and https://docs.python.org/3/library/sqlite3.html#controlling-transactions
        self._conn: sqlite3.Connection = sqlite3.connect(str(path), isolation_level=None)
        self._conn.row_factory = sqlite3.Row

        self.run_sql(self.SCHEMA_COLLECTIONS)
        self.run_sql(self.SCHEMA_LEXEMES)
        self.run_sql(self.SCHEMA_LUS)
        self.run_sql(self.SCHEMA_COLLECTIONS)

        self._load_lexicons_from_db()

    def __len__(self):
        """
            Returns the the total number of lexical units stored in the store.
        """
        return len(self._collection)

    def connection_can_close(self):
        self._conn.close()

    def ensure_connection(self):
        self._conn = sqlite3.connect(str(self._path))
        self._conn.row_factory = sqlite3.Row

    @property
    def path(self) -> Path:
        """
            The path where the db is stored (can also be ``':memory:'``)
        """
        return self._path

    @property
    def lexemes(self) -> Iterable[Lexeme]:
        """
            An iterator iterating over all lexemes.
        """
        return self._collection.lexemes

    @property
    def lexical_units(self) -> Iterable[LexicalUnit]:
        """
            An iterator iterating over all lexical units.
        """
        return self._collection.lexical_units

    @property
    def sources(self) -> Iterable[Path]:
        """
            A list of source files for the data in the db.
        """
        return [Path(p) for p in self._collection.lexicon_paths]

    @property
    def lexicons(self) -> Iterable[Lexicon]:
        """
            A list of lexicons in the db.
        """
        return self._collection.lexicons

    @property
    def collection(self) -> LexiconCollection:
        """
            The lexicon collection in the db.
        """
        return self._collection

    def id2lu(self, lu_id: str) -> LexicalUnit:
        """
            Returns the lexical unit with id given by `id`.

            Raises:
                KeyError: If a lexical unit with the id given does not exist.
        """
        return self._collection.id2lu(lu_id)

    def run_sql(self, sql: str, params: Optional[Iterable] = None) -> None:
        """
            Runs a sql query `sql` on the database and immediately closes
            the resulting cursor & commits changes.

            If the query contains placeholders (``?``) for values to be filled in,
            the function must be provided a second argument `params` which is an
            iterable of values to be substituted for the ``?`` in the query.
        """
        stime = time()
        log("sql_store:run_sql", logging.DEBUG, "Started query", sql, stime)
        with closing(self._conn.cursor()) as cursor:
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            self._conn.commit()
        log("sql_store:run_sql", logging.DEBUG, "Closed query", sql, time()-stime)

    @contextmanager
    def execute_sql(self, sql: str, params: Optional[Iterable] = None):
        """
            Executes the given sql query `sql` on the database and commits it.

            If the query contains placeholders (``?``) for values to be filled in,
            the function must be provided a second argument `params` which is an
            iterable of values to be substituted for the ``?`` in the query.

            Returns:
                A contextmanager yielding the result of the query (a sqlite cursor)
                and ensuring the cursor is closed.
        """
        stime = time()
        log("sql_store:execute_sql", logging.DEBUG, "Started query", sql, stime)
        ret = None
        try:
            if params:
                ret = self._conn.execute(sql, params)
            else:
                ret = self._conn.execute(sql)
            self._conn.commit()
            log("sql_store:execute_sql", logging.DEBUG, "Completed", sql, time()-stime)
            yield ret
        finally:
            if ret is not None:
                ret.close()
            log("sql_store:execute_sql", logging.DEBUG, "Closed query", sql, time()-stime)

    def remove_lexicon(self, lexicon: Lexicon):
        """
            Removes the lexicon `lexicon` from memory and from the database.
        """
        self._collection.remove_lexicon(lexicon)
        self.run_sql("DELETE FROM lexicons WHERE path = ?", (lexicon.path,))
        self.run_sql("DELETE FROM lexical_units WHERE lexicon = ?", (lexicon.path,))
        self.run_sql("DELETE FROM lexemes WHERE lexicon = ?", (lexicon.path,))

    def update_lexicon(self, lexicon: Lexicon):
        """
            Updates the lexicon `lexicon` in memory and in the database.
        """
        self._collection.update_lexicon(lexicon)
        version = time()
        self.run_sql("INSERT INTO lexicons(path, preamble, checksum, version) VALUES (?, ?, ?, ?)", (lexicon.path, dumps(lexicon._preamble), lexicon.checksum(), version))
        self.run_sql("DELETE FROM lexical_units WHERE lexicon = ?", (lexicon.path,))
        self.run_sql("DELETE FROM lexemes WHERE lexicon = ?", (lexicon.path,))
        rows = [(lex._id, lexicon._path, dumps(lex.comments), dumps(lex._src_start), dumps(lex._src_end)) for lex in lexicon.lexemes]
        stime = time()
        log("sql_store:run_sql", logging.DEBUG, "Inserting rows into lexemes", len(rows), stime)
        self._conn.execute("BEGIN TRANSACTION")
        self._conn.executemany("INSERT INTO lexemes(id, lexicon, comments, src_start, src_end) VALUES (?, ?, ?, ?, ?)", rows).close()
        self._conn.execute("COMMIT")
        log("sql_store:run_sql", logging.DEBUG, "Done Inserting rows into lexemes", len(rows), time()-stime)
        rows = [(lu._id, lu._parent._id, lexicon._path or '', dumps(lu)) for lu in lexicon.lexical_units]  # type: ignore
        stime = time()
        log("sql_store:run_sql", logging.DEBUG, "Inserting rows into lexical_units", len(rows), stime)
        self._conn.execute("BEGIN TRANSACTION")
        self._conn.executemany("INSERT INTO lexical_units(id, parent, lexicon, json_rep, version) VALUES (?, ?, ?, ?, "+str(version)+")", rows).close()
        self._conn.execute("COMMIT")
        log("sql_store:run_sql", logging.DEBUG, "Done Inserting rows into lexical_units", len(rows), time()-stime)

    def get_lexicon_version(self, lexicon: Lexicon):
        """
            Returns the version number of the lexicon `lexicon` in the database
        """
        with self.execute_sql("SELECT version FROM lexicons WHERE path = ?", (str(lexicon._path),)) as rows:
            return rows.fetchone()['version']

    def update_lexicon_version(self, lexicon: Lexicon):
        """
            Updates the version number (timestamp) of the lexicon given by `lexicon._path` in the DB to now.
        """
        self.run_sql("UPDATE lexicons SET version = ?, checksum = ? WHERE path = ?", (time(), str(lexicon._path), lexicon.checksum()))

    def changed_lexicons(self) -> Iterable[Lexicon]:
        """
            Returns a list of lexicons which contain changed lexical_units.
        """
        with self.execute_sql("""
            SELECT
                DISTINCT(lexicon.path)
            FROM
                lexical_units AS lu
            LEFT OUTER JOIN
                lexicons AS lexicon
            WHERE
                lu.lexicon = lexicon.path AND
                lu.version > lexicon.version
        """) as rows:

            return [self._collection.id2lexicon(row[0]) for row in rows]

    def update_lu(self, old_lu: LexicalUnit, new_lu: LexicalUnit, author: str):
        """
            Updates the lexical unit `old_lu` with the lexical unit `new_lu`.
        """
        self.refresh()
        self._collection.update_lu(old_lu, new_lu)
        self.run_sql("UPDATE lexical_units SET version = ?, author=?, json_rep=? WHERE id=?", (time(), author, dumps(new_lu), new_lu._id))
        return new_lu

    def lu_changed_since(self, timestamp: float) -> Iterable[LexicalUnit]:
        """
            Returns a list of lexical units changed (via :meth:`SQLStore.update_lu`) since
            the time given by `timestamp` (seconds since 1.1.1970, given by, e.g. time.time())
        """
        self.refresh()
        with self._lu_changed_since_cursor(timestamp) as rows:
            return [self._collection.id2lu(row['id']) for row in rows]

    def clear(self):
        """
            Deletes all data from the database and memory
        """
        self.run_sql("DELETE FROM lexicons")
        self.run_sql("DELETE FROM lexemes")
        self.run_sql("DELETE FROM lexical_units")
        self._collection = LexiconCollection()
        self._last_refresh = time()

    def refresh(self):
        """
            Synchronizes changes to lus in database with the in-memory representation.

            Note: Deleted lexical units will not be noticed by refresh
            and neither will adding new lexemes (and lus in those lexemes).
        """
        last_refresh = self._last_refresh
        self._last_refresh = time()
        with self._lu_changed_since_cursor(last_refresh) as rows:
            for row in rows:
                try:
                    old_lu = self.id2lu(row['id'])
                except KeyError:
                    old_lu = None
                try:
                    lu = loads(row['json_rep'])
                    lu._parent = self._collection.id2lex(row['parent'])
                    self._collection.update_lu(old_lu, lu)
                except KeyError:
                    log("server:sql_store", logging.WARN, "Not adding lu", row['id'], "because it belongs to a lexeme not present in memory.")

    def _lu_changed_since_cursor(self, timestamp: Optional[float]) -> ContextManager[sqlite3.Cursor]:
        if timestamp:
            return self.execute_sql("SELECT * FROM lexical_units WHERE version >= ?", (timestamp, ))

        return self.execute_sql("SELECT * FROM lexical_units")

    def _load_lexicons_from_db(self):
        self._collection = LexiconCollection()
        self._last_refresh = time()
        with self.execute_sql("SELECT path, preamble, checksum FROM lexicons") as rows:
            for lexicon_row in rows:
                # Load the lexemes
                lexs = {}
                with self.execute_sql("SELECT id, comments, src_start, src_end FROM lexemes WHERE lexicon = ?", (lexicon_row['path'],)) as lex_rows:
                    for lexeme_row in lex_rows:
                        lex = Lexeme(lexeme_row['id'])
                        lex.comments = loads(lexeme_row['comments'])
                        lex._src_start = loads(lexeme_row['src_start'])
                        lex._src_end = loads(lexeme_row['src_end'])
                        lexs[lex._id] = lex

                # Load the lexical units
                with self.execute_sql("SELECT parent, json_rep FROM lexical_units WHERE lexicon = ?", (lexicon_row['path'],)) as lu_rows:
                    for lu_row in lu_rows:
                        lex = lexs[lu_row['parent']]
                        lu = loads(lu_row['json_rep'])
                        lu._parent = lex
                        lex.lexical_units.append(lu)

                # Construct the Lexicon
                lexicon = Lexicon(lexs.values(), loads(lexicon_row['preamble']), lexicon_row['path'])
                lexicon._checksum = lexicon_row['checksum']
                self._collection.add_lexicon(lexicon)
