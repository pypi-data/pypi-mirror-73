import logging
import os
import sys
import tempfile
import threading

from pathlib import Path

from vallex import error
from vallex.cli.common import load_lexicons, save_lexicons
from vallex.cli.lib import main_command, option, root, sub_command
from vallex.grep import parse_pattern, filter_db
from vallex.log import log
from vallex.scripts import load_script_file, run_script, run_scripts, RES_ERROR
from vallex.scripts.mapreduce import create_table
from vallex.server import maint, utils
from vallex.server.app_state import AppState
from vallex.server.bottle_utils import WebAppFactory
from vallex.server.sql_store import SQLStore
from vallex.term import FG, RED, GREEN, STATUS, YELLOW
from vallex.vendor.bottle import WSGIRefServer  # type: ignore


@option('--no-browser', bool, help='Do not start a browser.')
@option('--pid-file', str, help='Write a pid of the server process to this file.', default='vallex-server.pid')
@option('--host', str, help='The hostname on which to listen to (defaults to localhost).')
@option('--port', int, help='The portname on which to listen to (defaults to 8080).')
@main_command()
def main(options={}):
    """Run the web server backend."""

    lexicon_files = options.get('load-lexicons', [])
    if lexicon_files:
        # If there are input files specified on the command line
        # we create a temporary store and initialize it with the
        # data from the inputs and then pass that to the webapp
        coll = load_lexicons(options)
        _, store_path = tempfile.mkstemp(suffix='.db')
        store = SQLStore(store_path)
        maint.webdb_migrate(store)
        maint.webdb_addlexicons(store, coll.lexicons)
        remove_db_on_exit = True
        root.config.web_db = Path(store_path)
        root.config.web_lexicons = [Path(lexicon._path) for lexicon in coll.lexicons]
    else:
        remove_db_on_exit = False
        store = SQLStore(root.config.web_db)
        maint.webdb_migrate(store)
        maint.webdb_update(store)
        maint.webdb_addlexicons(store, root.config.web_lexicons)

    # Need this to register the routes
    import vallex.server.views

    state = AppState(root.config, store)
    webapp = WebAppFactory.create_app(state)

    pid_file = Path(options['pid-file'])

    host = options.get('host', root.config.web_host)
    port = options.get('port', root.config.web_port)
    try:
        pid_file.write_text(str(os.getpid()))

        # If the port is specified on the command line
        # we want to fail if we cannot listen on it
        # otherwise, we just find the first free port
        # above the one given in the config file
        if 'port' not in options:
            port = utils.find_free_port(port)
        server = WSGIRefServer(host=host, port=port)
        server_thread = threading.Thread(target=server.run, args=[webapp])
        server_thread.start()
        if not options['no-browser']:
            utils.wait_for_port(port)
            import webbrowser
            webbrowser.open('http://'+host+':'+str(port))
            server_thread.join()
    finally:
        pid_file.unlink()
        if remove_db_on_exit:
            Path(store_path).unlink()

    return 0


@sub_command()
def sync_db(options={}):
    """
        Saves user edits present in the web db back into the lexicon files and loads any
        changes from the lexicon files into the db and any new lexicons specified in the
        config.
    """
    store = SQLStore(root.config.web_db)
    maint.webdb_migrate(store)
    for lexicon in store.changed_lexicons():
        if lexicon.changed_on_disk(since=store.get_lexicon_version(lexicon)):
            STATUS.print("File", lexicon._path, "changed by another application, moving it to",
                         lexicon._path+'.backup', "and overwriting with the web version")
            Path(lexicon._path).rename(lexicon._path+'.backup')
        lexicon.write_to_disk()
        store.update_lexicon_version(lexicon)
    maint.webdb_addlexicons(store, root.config.web_lexicons)
    STATUS.print("sync_db finished successfully.")
    return


@sub_command()
def reset_db(options={}):
    """
        Recreates the database and loads the lexicons specified in the config
        into the newly created db.
    """
    STATUS.start_action("Removing db")
    Path(root.config.web_db).unlink()
    STATUS.end_action()

    store = SQLStore(root.config.web_db)
    maint.webdb_migrate(store)
    maint.webdb_addlexicons(store, root.config.web_lexicons)
    return


@sub_command()
def migrate_db(options={}):
    """Migrates the database schema to the latest version.."""
    store = SQLStore(root.config.web_db)
    maint.webdb_migrate(store)
    return


@sub_command()
def applied_migrations(options={}):
    """Prints out a list of migrations which were applied."""
    store = SQLStore(root.config.web_db)
    STATUS.print("Applied migrations:")
    for m_id in maint.get_applied_migrations(store):
        STATUS.print("    ", m_id)
    return


@sub_command()
def show_migrations(options={}):
    """Shows the status of the database schema migrations."""
    store = SQLStore(root.config.web_db)
    applied = maint.get_applied_migrations(store)
    migrations = maint.available_migrations()
    available = {m_id for m_id, _ in migrations}
    available_unapplied = available.difference(applied)
    STATUS.print("Available migrations:")
    for m_id, m in migrations:
        if m_id in applied:
            if m_id in available:
                m_id = FG(GREEN) | m_id
            deps = "["+','.join(m.DEPENDS)+"]" if m.DEPENDS else ""
            STATUS.print("    ", m_id, deps)
        else:
            applied_deps = [FG(GREEN) | dep for dep in m.DEPENDS if dep in applied] if m.DEPENDS else []
            available_unapplied_deps = [FG(YELLOW) | dep for dep in m.DEPENDS if dep in available_unapplied] if m.DEPENDS else []
            missing_deps = [FG(RED) | dep for dep in m.DEPENDS if dep in m.DEPENDS and dep not in available and dep not in applied] if m.DEPENDS else []
            deps = "["+','.join(applied_deps+available_unapplied_deps+missing_deps)+"]" if m.DEPENDS else []
            STATUS.print("    ", FG(YELLOW) | m_id, deps)
    return
