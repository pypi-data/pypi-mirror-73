""" WebApp database maintenance scripts.




    This module implements methods for maintaining the web app database (sqlstore), in particular
    initializing, loading, updating and migrating the db schema.


    List of functions
    -----------------

    - :func:`webdb_addlexicons` adds lexicons to the database
    - :func:`webdb_migrate` runs migrations on the database
    - :func:`webdb_update` updates the database

    List of Classes
    ---------------

    - :class:`DBMigration` a base class for all db migrations (schema changes)

"""
import logging

from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple, Union

from vallex import Config, Lexicon, load_lexicon
from vallex.log import log
from vallex.term import STATUS
from vallex.utils import _import_python_file

from .sql_store import SQLStore

_MESSAGES_TABLE_SCHEMA = """
    CREATE TABLE IF NOT EXISTS messages (
        content TEXT,
        author TEXT,
        timestamp REAL
    )
"""
"SQL Schema for a table holding messages to be displayed to the user by the frontend app."

_SEARCH_STATS_TABLE_SCHEMA = """
    CREATE TABLE IF NOT EXISTS search_stats (
        key TEXT,
        pattern TEXT,
        user TEXT,
        count INTEGER,
        UNIQUE (key, pattern, user)
    )
"""
"SQL Schema for a table holding stats on search query popularity"

_HIST_STATS_TABLE_SCHEMA = """
    CREATE TABLE IF NOT EXISTS hist_stats (
        key TEXT,
        pattern TEXT,
        user TEXT,
        count INTEGER,
        UNIQUE (key, pattern, user)
    )
"""
"SQL Schema for a table holding stats on histogram query popularity"

_MIGRATIONS_TABLE_SCHEMA = """
    CREATE TABLE IF NOT EXISTS applied_migrations (
        id TEXT
    )
"""


class DBMigration:
    """
        A utility class for defining database migrations.

        Attributes:
            APPLY_SQL[str]:     the sql which is run on the database by the base `:meth:DBMigration.apply` method
                                implementation to apply the migration.
            ROLLBACK_SQL[str]:  the sql which is run on the database by the base `:meth:DBMigration.rollback` method
                                implementation to unapply the migration.
            DEPENDS[List[str]]: the list of migration ids which must be applied before this migration can be applied;
                                the id of the migration is the file name which contains its definition, followed by a
                                colon and the name of the migration class (e.g. ``user_table.py:AddUserTable``)

        Example::

            class AddSessionTable(DBMigration):
                APPLY_SQL = \"""
                        CREATE TABLE IF NOT EXISTS users (
                            key TEXT,
                            pattern TEXT,
                            user TEXT,
                            count INTEGER,
                            UNIQUE (key, pattern, user)
                        )
                \"""
                ROLLBACK_SQL = \"""
                        DROP TABLE hist_stats;
                \"""
    """
    APPLY_SQL = ""
    ROLLBACK_SQL = ""
    DEPENDS: Optional[Iterable[str]] = None

    @classmethod
    def apply(cls, store: SQLStore):
        """
            Applies the migration to the sqlstore `store`.

            The base implementation just runs the sql :attr:`DBMigration.APPLY_SQL` on the store.
        """
        store.run_sql(cls.APPLY_SQL)

    @classmethod
    def rollback(cls, store: SQLStore):
        """
            Un-Applies the migration to the sqlstore `store`.

            The base implementation just runs the sql :attr:`DBMigration.ROLLBACK_SQL` on the store.
        """
        store.run_sql(cls.ROLLBACK_SQL)


def webdb_addlexicons(store: SQLStore,  lexicons: List[Union[Path, Lexicon]]):
    """
        Adds the specified `lexicons` to the `store`.

        Each lexicon to be added may be either an instance of :class:`Lexicon <vallex.data_structures.collections.Lexicon>`,
        or specified by a path. In the latter case it is first loaded from that path.
    """
    STATUS.print("Adding lexicon sources to db ...")
    for lexicon_path in [lp for lp in lexicons if isinstance(lp, Path) and lp not in store.sources]:
        with lexicon_path.open('r', encoding='utf-8') as LEXICON_SRC:
            progress = STATUS.progress_bar("Loading "+lexicon_path.name)
            updated_lexicon = load_lexicon(LEXICON_SRC, progress_cb=progress.update)
            progress.done()
        store.update_lexicon(updated_lexicon)
    STATUS.start_action("Adding loaded lexicons to db ...")
    for lexicon in [lp for lp in lexicons if isinstance(lp, Lexicon)]:
        store.update_lexicon(lexicon)
    STATUS.end_action()


def _apply_ready(store: SQLStore, migrations: List[Tuple[str, DBMigration]], applied: Set[str]):
    """
        Applies migrations from the list `migrations`, which have satisfied dependencies (i.e.
        each of whose dependency is present in `applied`) to `store`.

        Returns: A boolean indicating whether any migrations were successfully applied and a
                 dictionary, keyed by migration id, which contains migrations whose
                `:meth:DBMigration.apply` method raised an exception.
    """
    progress = False
    failed = {}
    for (m_id, m) in migrations:
        if m.DEPENDS:
            m.DEPENDS = set(m.DEPENDS).difference(applied)
        if not m.DEPENDS and not hasattr(m, '_applied'):
            STATUS.start_action("Applying db migration", m_id)
            try:
                m.apply(store)
            except Exception as ex:
                STATUS.end_action(ok=False)
                STATUS.print("Error:", ex)
                failed[m_id] = (m, ex)
            else:
                store.run_sql("INSERT INTO applied_migrations(id) VALUES (?)", (m_id,))
                applied.add(m_id)
                progress = True
                STATUS.end_action()
    return progress, failed


def available_migrations() -> List[Tuple[str, DBMigration]]:
    """
        Loads database migrations from the ``db_migrations`` subdirectory,
        and returns them as a list of pairs ``(migration_id, migration)``.

        Each migration should be defined in a python file in the ``db_migrations``
        subdirectory and should be a subclass of `:class:DBMigration`. Its id
        will be the name of the file where it is defined, followed by a colon and
        the name of the class.
    """
    ret: List[Tuple[str, DBMigration]] = []
    for path in (Path(__file__).parent/'db_migrations').glob("*.py"):
        try:
            mod = _import_python_file('vallex.scripts', path)
            for attr in dir(mod):
                val = getattr(mod, attr)
                if isinstance(val, type) and issubclass(val, DBMigration) and not val == DBMigration:
                    ret.append((path.name+':'+val.__name__, val))  # type: ignore
        except Exception as err:
            log('vallex.server.db', logging.ERROR, "Error loading db migration from", path, ":", err)
    return ret


def get_applied_migrations(store: SQLStore) -> Set[str]:
    """
        Returns the list of migration_ids which were applied (in the past) to the `store`.
        These are stored in the ``applied_migrations`` table in the database.
    """
    with store.execute_sql("SELECT id FROM applied_migrations") as rows:
        return {row['id'] for row in rows}


def webdb_migrate(store: SQLStore) -> Dict[str, List[Tuple[str, DBMigration, Any]]]:
    """
        Runs datbase migrations on the store so that the expected table
        structure is present.

        Returns: A dictionary of failed migrations. The dictionary has two keys: ``deps``
                 and ``other``. The ``deps`` key stores a list of triples of the form
                 ``(migration_id, migration, missing_dependencies)``, one for each migration
                 which failed due to unsatisfied dependencies . The ``other`` key stores
                 list of triples ``(migration_id, migration, exception)`` one for each
                 migration whose `:meth:DBMigration.apply` method raised an exception.
    """
    STATUS.start_action("Ensuring basic DB schema")
    store.run_sql(_MESSAGES_TABLE_SCHEMA)
    store.run_sql(_SEARCH_STATS_TABLE_SCHEMA)
    store.run_sql(_HIST_STATS_TABLE_SCHEMA)
    store.run_sql(_MIGRATIONS_TABLE_SCHEMA)
    STATUS.end_action()

    migrations = available_migrations()
    applied = get_applied_migrations(store)

    failures: Dict[str, Tuple[DBMigration, Exception]] = {}
    progress = True
    while progress:
        progress, failed = _apply_ready(store, migrations, applied)
        failures.update(failed)
        migrations = [(mid, m) for mid, m in migrations if mid not in failures and mid not in applied]

    for m_id, deps in [(m_id, m.DEPENDS) for m_id, m in migrations if m.DEPENDS]:
        STATUS.print("Failed applying", m_id, ": missing dependencies", ",".join(deps))  # type: ignore

    return {
        'deps': [(m_id, m, m.DEPENDS) for (m_id, m) in migrations],
        'other': [(m_id, m, ex) for m_id, (m, ex) in failures.items()]
    }


def webdb_update(store: SQLStore):
    """
        Updates the store by checking for lexicons that have changed on disk
        and reloading them. Additionally, if the database contains unsaved
        changes, it first saves them to a backup file.
    """
    STATUS.start_action("Testing for changes on disk")
    changed = [lexicon._path for lexicon in store.changed_lexicons()]
    ch_on_disk = []

    for lexicon in list(store.lexicons):
        STATUS.update(lexicon.path)
        if lexicon.changed_on_disk(since=store.get_lexicon_version(lexicon)):
            ch_on_disk.append(lexicon.path)
            if lexicon.path in changed:
                lexicon.write_to_disk(backup=True)
                store.run_sql("INSERT INTO messages(content, author, timestamp) VALUES (?, ?, strftime('%s','now'))", ("Unsaved changes to "+str(lexicon._path)+" saved to "+str(lexicon._path)+".backup", 'web'))
            if not Path(lexicon._path).exists():
                store.remove_lexicon(lexicon)
            else:
                with Path(lexicon._path).open('r', encoding='utf-8') as LEXICON_SRC:
                    progress = STATUS.progress_bar("Loading "+lexicon._path)
                    updated_lexicon = load_lexicon(LEXICON_SRC, progress_cb=progress.update)
                    progress.done()
                store.update_lexicon(updated_lexicon)

    STATUS.end_action()
    STATUS.print("Lexicons with unsaved changes:", changed)
    STATUS.print("Lexicons with changes on disk:", ch_on_disk)
