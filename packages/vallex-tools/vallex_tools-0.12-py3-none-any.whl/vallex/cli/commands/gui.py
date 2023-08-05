import logging
import os
import sys
import tempfile

import vallex.term

from pathlib import Path

from vallex.cli.common import load_lexicons
from vallex.cli.lib import main_command, option, root, sub_command
from vallex.config import FROZEN, SCRIPT, __version__
from vallex.server import maint
from vallex.server.sql_store import SQLStore
from vallex.term import STATUS, FG, GREEN, YELLOW, RED
from vallex.log import log

try:
    from vallex.updater import Updater
    UPDATER_AVAILABLE = True
except Exception as ex:
    UPDATER_AVAILABLE = False
    _UPDATER_ERROR = ex
    log("cli:gui", logging.DEBUG, "Could not import updater", _UPDATER_ERROR)

try:
    from PyQt5.QtWidgets import QApplication  # type: ignore
    from PyQt5.QtGui import QIcon  # type: ignore

    from vallex.gui.main_window import MainWindow

    GUI_AVAILABLE = True
except Exception as ex:
    GUI_AVAILABLE = False
    _GUI_ERROR = ex
    log("cli:gui", logging.DEBUG, "Could not import PyQt", _GUI_ERROR)


@main_command()
def main(options={}):
    """Run the QtWebEngine based gui."""
    if not GUI_AVAILABLE:
        STATUS.print("GUI not available", _GUI_ERROR)
        log("cli:gui", logging.ERROR, "Could not import PyQt", _GUI_ERROR)
        return -1

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

    if sys.platform == 'win32' and FROZEN:
        # This is needed to enable QtWebEngine process
        # to find Qt dlls.
        os.environ['PATH'] += ';'+sys._MEIPASS
    _qtapp = QApplication(sys.argv)
    _qtapp.setWindowIcon(QIcon(str(Path(__file__).parent.parent.parent/'pyvallex.ico')))
    gui = MainWindow(root.config, store)
    vallex.term.MODE = vallex.term.IOMode.QT
    ret = _qtapp.exec_()
    gui.app_server.stop()
    return ret


@sub_command()
def check_updates(options={}):
    """Updates the frozen binary to the latest version."""
    if not UPDATER_AVAILABLE:
        STATUS.print(FG(RED) | "Updater functionality not available (nacl or bsdiff library not present?)")
        STATUS.print(FG(RED) | "Error:", _UPDATER_ERROR)
        log("cli:gui", logging.DEBUG, "Could not import updater", _UPDATER_ERROR)
        return -1
    updater = Updater(root.config.release_key, root.config.release_url, SCRIPT, __version__)
    STATUS.start_action("Checking for updates at "+root.config.release_url)
    updater.check_for_updates()
    STATUS.end_action()
    upd, sz = updater.available_update()
    if upd:
        STATUS.print("Update available:", FG(YELLOW) | str(upd), FG(GREEN) | str(int(sz/10**6))+" Mb")
