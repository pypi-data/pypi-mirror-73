import logging
import sys

import vallex.term

from pathlib import Path
from typing import Optional

from PyQt5.QtCore import pyqtSlot, QUrl  # type: ignore
from PyQt5.QtGui import QIcon  # type: ignore
from PyQt5.QtWidgets import qApp, QFileDialog, QMainWindow  # type: ignore

from vallex.config import __version__, Config, SCRIPT, SCRIPT_DIR, FROZEN
from vallex.gui.app_menu import AppMenu
from vallex.gui.qtutils import BackgroundTask
from vallex.gui.status import Status, StatusProxy
from vallex.gui.tab_widget import TabWidget
from vallex.server import maint
from vallex.server.wsgi_app_server import AppServer
from vallex.server.sql_store import SQLStore
from vallex.term import FG, STATUS, YELLOW, GREEN, RED
from vallex.log import log

try:
    from vallex.updater import Updater
    _HAVE_UPDATER = True
except Exception as ex:
    _HAVE_UPDATER = False
    log("gui", logging.WARN, "Could not import updater", ex)


class MainWindow(QMainWindow):
    _LAST_MESSAGE_ID = 0

    def __init__(self, config: Config, store: Optional[SQLStore] = None):
        super().__init__()
        self._loaded = False
        self.vallex_config = config
        self.store = store or SQLStore(self.vallex_config.web_db)
        # FIXME: The next line fails if no release_key available
        self.updater = Updater(config.release_key, config.release_url, SCRIPT, __version__) if _HAVE_UPDATER else None

        # NOTE: The AppServer __must__ get a new SQLStore since
        # it will be used in a different thread and SQLite does
        # not allow using the same db connection from different
        # threads
        self.app_server = AppServer(self.vallex_config, SQLStore(self.vallex_config.web_db))
        self.app_server.start()

        app_menu = AppMenu(self)

        self.setGeometry(10, 10, 800, 800)
        self.setWindowTitle('NomVallex')

        self.STATUS = Status(self.statusBar())
        self.status_proxy = StatusProxy(self.STATUS)
        vallex.term.STATUS.set_impl(self.status_proxy)

        self.tabs = TabWidget(QUrl(self.app_server.url))
        self.setCentralWidget(self.tabs)
        self.show()

    def on_page_load(self):
        self._loaded = True
        self.setWindowTitle(self.webView.page().title())

    def run_action(self, action: str):
        if self._loaded:
            self.webView.page().runJavaScript("app_store.actions."+action)

    @AppMenu.item('&File', '&Open Vallex Repository', shortcut='Ctrl+O')
    def set_vallex_location(self):
        directory = QFileDialog.getExistingDirectory(self, caption='Select Vallex Repository', directory=str(self.vallex_config.vallex_repo), options=QFileDialog.Options())
        if directory:
            repo_location = Path(directory)
            if repo_location.is_dir() and str(repo_location) != str(self.vallex_config.vallex_repo):
                self.vallex_config.vallex_repo = repo_location
                (SCRIPT_DIR/'pyvallex.ini').write_text(str(self.vallex_config), encoding='utf-8')
                self.reload_lexicons()

    @AppMenu.item('&File', '&New Tab', icon='document-new', shortcut='Ctrl+Shift+T')
    def new_tab(self): self.tabs.new_tab(QUrl(self.app_server.url))

    @AppMenu.item('&File', '&Save Lexicons', icon='document-save', shortcut='Ctrl+S')
    def save_lexicons(self):
        """Saves user edits present in the web db back into the lexicon files."""
        self.store.refresh()
        for lexicon in self.store.changed_lexicons():
            if lexicon.changed_on_disk(since=self.store.get_lexicon_version(lexicon)):
                self.STATUS.print("File", lexicon._path, "changed by another application, moving it to", lexicon._path+'.backup', "and overwriting with the web version")
                suffix = 0
                while Path(lexicon._path+'.backup'+str(suffix)).exists():
                    suffix += 1
                Path(lexicon._path).rename(lexicon._path+'.backup'+str(suffix))
            lexicon.write_to_disk()
            self.store.update_lexicon_version(lexicon)

    @AppMenu.item('&File', '&Save Results to PDF', icon='application-pdf', shortcut='Ctrl+P')
    def print_results(self): self.tabs.print_results()

    AppMenu.separator('&File')

    @AppMenu.item('&File', 'Reload Lexicons', icon='view-refresh')
    def reload_lexicons(self):
        self.tabs.run_action_in_all_tabs("show_busy_dialog()")
        task = self._reload_lexicons()
        task.done.connect(self.reload_all_tabs)
        task.start()

    @AppMenu.item('&File', '&Reload Current Tab', icon='view-refresh', shortcut='Ctrl+R')
    def reload_current_tab(self): self.tabs.reload_current_tab()

    @pyqtSlot()
    def reload_all_tabs(self):
        self.STATUS.print("Reloading tabs")
        self.tabs.reset_url(QUrl(self.app_server.url))

    AppMenu.separator('&File')

    @AppMenu.item('&File', '&Close Current Tab', icon='application-exit', shortcut='Ctrl+W')
    def close_current_tab(self): self.tabs.close_current_tab()

    @AppMenu.item('&File', '&Quit', icon='application-exit', shortcut='Ctrl+Q')
    def quit(self):
        self.app_server.stop()
        qApp.quit()

    @AppMenu.item('&View', 'Compute Histograms')
    def show_stats(self): self.tabs.show_stats()

    @AppMenu.item('&View', 'Show LU Sources')
    def toggle_sources_display(self):
        self.tabs.toggle_sources_display()
        self.tabs.current_tab_page().runJavaScript("app_store.state.gui.show_source", AppMenu.toggle_title(
            self.toggle_sources_display.__action__,
            'Show Formatted LUs',
            'Show LU Sources'
        ))

    @AppMenu.item('&View', 'Show All LUs')
    def toggle_show_all_lus(self):
        if self._loaded:
            self.tabs.toggle_show_all_lus()
            self.tabs.current_tab_page().runJavaScript("app_store.state.gui.show_all_lus", AppMenu.toggle_title(
                self.toggle_show_all_lus.__action__,
                'Show Only Matched LUs',
                'Show All LUs'
            ))

    @AppMenu.item('&Settings', '&Display Preferences')
    def show_display_settings(self): self.tabs.show_display_settings()

    if FROZEN and _HAVE_UPDATER:
        @BackgroundTask
        def download_update(self):
            progress = STATUS.progress_bar("Downloading updates")
            self.updater.download_update(progress.update)
            progress.done()

        @pyqtSlot()
        def finish_update(self, confirm=True):
            if confirm:
                self.STATUS.show_message("Application needs to restart...", {"RESTART": lambda: self.finish_update(confirm=False)})
                return
            self.STATUS.print("Stopping server")
            self.app_server.stop()
            self.STATUS.print("Quitting application")
            qApp.quit()
            STATUS.print("Applying update")
            self.updater.apply_update()

        @pyqtSlot()
        def start_update(self):
            self.STATUS.print("Downloading update")
            task = self.download_update()
            task.failed.connect(lambda ex: self.tabs.notify("Updating to {ver} failed with error: {err}".format(ver=str(self.updater.available_update()[0]), err=str(ex))))
            task.done.connect(self.finish_update)
            task.start()

        @pyqtSlot()
        def on_update_check_done(self):
            info = self.updater.available_update()
            if info:
                update, size = info
                self.STATUS.print("Update available:", FG(YELLOW) | str(update))
                self.STATUS.show_message("A new version of the program is available (need to download "+str(int(size/(10**6)))+" Mb): "+str(update), {"UPDATE": self.start_update, "NOT NOW": None})

        @AppMenu.item('&Settings', 'Check for updates')
        def check_for_updates(self):
            self.STATUS.print("Checking for updates")
            task = BackgroundTask(self.updater.check_for_updates)()
            task.failed.connect(lambda ex: self.tabs.notify("Error checking for updates: " + str(ex)))
            task.done.connect(self.on_update_check_done)
            task.start()

    @AppMenu.item('&Help', '&About NomVallex')
    def show_about(self): self.tabs.show_about()

    @BackgroundTask
    def _reload_lexicons(self):
        # We are running in a background thread so we can't do
        # self.store = ... here (because sqlite connections can
        # only be used from the thread they were created in)
        store = SQLStore(self.vallex_config.web_db)
        maint.webdb_migrate(store)
        maint.webdb_update(store)
        self.vallex_config.update_lexicon_dirs()
        self.vallex_config.update_lexicon_lists()
        maint.webdb_addlexicons(store, self.vallex_config.web_lexicons)

        # We copy the in-memory representation from store
        # to self.store;
        # FIXME: This should be refactored into a method
        # in SQLStore
        self.store._collection = store._collection
        self.store._last_refresh = store._last_refresh

        # Restart the backend
        old_port = self.app_server.port
        self.app_server.stop()
        self.app_server = AppServer(self.vallex_config, SQLStore(self.vallex_config.web_db))
        if sys.platform == 'win32':
            # FIXME: For some reason, on windows the old port is not closed
            # (because of https://stackoverflow.com/questions/15260558/python-tcpserver-address-already-in-use-but-i-close-the-server-and-i-use-allow ?)
            # and the utils.find_free_port method does not discover this (because we are in the same process?)
            # so we increase the port number by one and hope for the best
            self.app_server.port = old_port + 1
        self.app_server.start()
