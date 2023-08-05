""" SQL Store




    This file provides the implementation of the AppState class which holds all
    the data that the running web app needs to have access to
    (the lexicons, ...)
"""
import sqlite3
import sys

from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from vallex import load_lexicon, Config, __version_info__
from vallex.config import VALLEX_PACKAGE_PATH
from vallex.json_utils import load as json_load
from vallex.term import STATUS
from vallex.scripts import load_scripts, Script, prepare_requirements, run_scripts, SCRIPTS

from .sql_store import SQLStore

_CURRENT_DIR = VALLEX_PACKAGE_PATH / 'server'

_FRONTEND_DIR = _CURRENT_DIR / 'frontend'


class AppState:
    """
        An instance of this class holds all the data that the running web app
        needs to have access to.

        Attributes:
            index_html: the contents of the main index.html file
            frontend_config: a dict which contains frontend configuration
                             (this is exposed to the frontend javascript on the '/api/config'
                             endpoint)
            config: A ConfigParser object containing the vallex configuration read
                    from an ini file
            store:  An instance of the :class:`SQLStore <.sql_store.SQLStore>` class
                    containing lexicon data
            vallex: An instance of the :class:`AppState.Vallex` class containing
                    metadata about the lexicons (currently the list of distinct lu attribute names)
                    plus (info about) data-validation tests
    """

    @property
    def STATIC_DIR(self):
        "The directory where the frontend assets (js, css, png files) are located"
        return self.config.web_dist_dir / 'static'

    class Vallex:
        """
            Holds information about vallex data. An instance of this
            class is available as the :attr:`AppState.vallex` attribute
            of an :class:`AppState` instance.
        """

        attrs: List[Tuple[str, str]] = []
        "A list of distinct attribute names present in lexical units"

        attr_popularity: Dict[str, Dict[str, int]] = {
            'search': defaultdict(int),
            'histogram': defaultdict(int)
        }
        "A table storing the popularity of search/histogram keys"

        tests: List[Script] = []
        "A list of available data-validation tests (functions)"

        lex_tests: List[Tuple[str, Script]] = []
        "A list of lexeme validation tests as pairs (test_name, test)"

        lu_tests: List[Tuple[str, Script]] = []
        "A list of lexical unit validation tests as pairs (test_name, test)"

        version: Tuple[str, str, str] = ('Unknown', 'Unknown', 'Unknown')
        "The svn version, date and repo url of last change of the data repo."

    def __init__(self, config: Config, store: SQLStore):
        """
            Initializes the application state.

            The following steps need to be performed:

            1. Loads the index.html & webui-config files

            2. Computes the set of lexical attribute names present in the lexicon and stores them
               in the :attr:`vallex.attribs` property.

            3. Loads the data validation tests for lexemes and lexical units storing them in
               :attr:`vallex.lex_tests` and :attr:`vallex.lix_tests` properties, respectively.
               Moreover it stores all of the tests in the :attr:`vallex.tests` property.
               Then, it extends the list :attr:`vallex.attribs` with names of the tests prefixed
               by `error.`.

            4. It runs the tests and stores the resulting errors as properties on the lexical units
               and lexemes
        """
        self.config = config
        self.store = store

        git_hash, git_tag, git_date = __version_info__
        self.backend_version = {
            'hash': git_hash,
            'tag': git_tag,
            'date': git_date,
            'vallex_version': self.config.get_repo_version()
        }

        STATUS.start_action("Reading frontend configuration")

        self.frontend_config = json_load(config.web_ui_config.open('r', encoding='utf-8'))
        self.frontend_config['mode'] = self.config.web_mode
        self.HELP_DIR = _FRONTEND_DIR / 'help'
        self.help_toc = json_load((self.HELP_DIR/'toc.json').open('r', encoding='utf-8'))
        STATUS.end_action()
        STATUS.print("Frontend dir:", _FRONTEND_DIR)
        STATUS.print("Static dir:", self.STATIC_DIR)
        STATUS.print("Help dir:", self.HELP_DIR)

        # Populate the vallex attribute (list of lu attributes, tests, results of tests)
        self.vallex = self.Vallex()
        self.vallex.version = self.config.get_repo_version()

        STATUS.start_action('Loading scripts')
        STATUS.update('loading')
        load_scripts(self.config.script_dirs)
        STATUS.end_action()
        self.vallex.lex_tests = SCRIPTS.get('test.lexeme', [])
        self.vallex.lu_tests = SCRIPTS.get('test.lu', [])

        STATUS.start_action("Computing script requirements")
        prepare_requirements(self.config, self.store.collection)
        STATUS.end_action()

        progress = STATUS.progress_bar("Running test scripts")
        _, failures = run_scripts(self.store.collection, 'test', progress.update)
        progress.done()

        for test_name, obj, message in failures:
            obj._errors.append((test_name, str(message)))

        progress = STATUS.progress_bar("Computing dynamic properties")
        stats, _ = run_scripts(self.store.collection, 'compute', progress.update)
        if 'compute' in stats:
            failed = [(scr_name, res['error']) for scr_name, res in stats['compute'].items() if res['error']]
            if failed:
                progress.done(str(failed))
            else:
                progress.done()
        else:
            progress.done()

        STATUS.start_action("Finding search match keys")
        self.vallex.attrs.extend({k for lu in self.store.lexical_units for k in lu.match_keys()})
        STATUS.update("Updating search key popularity.")
        self._refresh_key_popularity('search', user='web')
        STATUS.update("Updating histogram key popularity.")
        self._refresh_key_popularity('histogram', user='web')
        STATUS.end_action()

        self.vallex.attrs.extend([('error.'+tname, test.__doc__ or '') for tname, test in self.vallex.lu_tests])
        self.vallex.attrs.sort(key=lambda attr: (-self.vallex.attr_popularity['search'][attr[0]], int('.' in attr[0]), attr[0]))

        self.vallex.tests.extend([ch for chn, ch in self.vallex.lex_tests+self.vallex.lu_tests])

    _table_map = {
        'search': 'search_stats',
        'histogram': 'hist_stats'
    }

    def update_stat(self, key: str, pattern: str, table: str, user: str = 'web'):
        """
            Increments the use count for the (`key`,`pattern`) pair in table `table`,
            where table is either ``search`` or ``histogram``.
        """
        self.vallex.attr_popularity[table][key] += 1
        sql_table = self._table_map[table]
        try:
            self.store.run_sql("INSERT INTO {} (key, pattern, user, count) VALUES (?, ?, ?, 1)".format(sql_table), (key.strip().lower(), pattern.strip(), user))
            needs_update = False
        except sqlite3.IntegrityError:
            needs_update = True
        if needs_update:
            self.store.run_sql("UPDATE {} SET count = count + 1 WHERE key = ? AND pattern = ? AND user = ?".format(sql_table), (key.strip().lower(), pattern.strip(), user))
        self.vallex.attr_popularity[table][key] += 1

    def _refresh_key_popularity(self, table: str, user: str = 'web'):
        """Updates the vallex.attr_popularity map from the database. """
        sql_table = self._table_map[table]
        with self.store.execute_sql("SELECT key, sum(count) AS count FROM {} WHERE user = ? GROUP BY key".format(sql_table), (user,)) as rows:
            for row in rows:
                self.vallex.attr_popularity[table][row['key']] = row['count']

    def add_message(self, *args, author: str = 'web') -> None:
        """
            Saves a message for display in the frontend.

            The function converts the elements of `args` to string and then
            concatenates them. The resulting message is stored into the database
            from which it may be later retrieved and sent to the frontend app.
        """
        msg = ' '.join([str(a) for a in args])
        self.store.run_sql("INSERT INTO messages(content, author, timestamp) VALUES (?, ?, strftime('%s','now'))", (msg, author))
