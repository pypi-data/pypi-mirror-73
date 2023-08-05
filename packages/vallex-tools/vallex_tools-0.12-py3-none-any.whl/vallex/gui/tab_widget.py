from functools import wraps
from typing import List, Optional

from PyQt5.QtCore import pyqtSlot, QUrl  # type: ignore
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings  # type: ignore
from PyQt5.QtWidgets import QFileDialog, QTabWidget  # type: ignore

from vallex.gui.bridge import JSCallReceiver


def StoreAction(method):
    @wraps(method)
    def decorated(self, *args: List[str]):
        jsargs = ','.join(['"'+str(a)+'"' for a in args])
        self.run_action(method.__name__+"({args})".format(args=jsargs))
    return decorated


class TabWidget(QTabWidget):
    def __init__(self, url: QUrl):
        super().__init__()
        self._url = url
        self.setTabBarAutoHide(True)
        self.setTabsClosable(False)
        self.tabCloseRequested.connect(self._tab_close)
        self.new_tab(url)

    def new_tab(self, url: Optional[QUrl] = None):
        tab = SingleTab(self, url)
        self.addTab(tab, "NomVallex")
        if self.count() > 1:
            self.setTabsClosable(True)
        return tab

    def run_action(self, action: str):
        tab = self.currentWidget()
        if tab._loaded:
            tab.page().runJavaScript("app_store.actions."+action)

    def run_action_in_all_tabs(self, action: str):
        for index in range(self.count()):
            tab = self.widget(index)
            if tab._loaded:
                tab.page().runJavaScript("app_store.actions."+action)

    def reset_url(self, url: QUrl):
        self._url = url
        self.reload_all_tabs()

    def print_results(self):
        # TODO: Warn the user if there are more than 200 lexemes in the results
        tab = self.currentWidget()
        if tab._loaded:
            self.run_action('set_result_pagination(200)')
            fname, _ = QFileDialog.getSaveFileName(self, caption='Save as PDF')
            if fname:
                tab.page().printToPdf(fname)
            self.run_action('set_result_pagination(10)')

    def reload_current_tab(self):
        tab = self.currentWidget()
        tab._loaded = False
        tab.page().load(self._url)

    @pyqtSlot()
    def reload_all_tabs(self):
        for index in range(self.count()):
            tab = self.widget(index)
            tab._loaded = False
            tab.page().load(self._url)

    def current_tab_page(self):
        return self.currentWidget().page()

    def close_current_tab(self):
        if self.count() > 1:
            self.removeTab(self.currentIndex())

    @StoreAction
    def show_stats(self): pass

    @StoreAction
    def show_display_settings(self): pass

    @StoreAction
    def notify(self, msg): pass

    @StoreAction
    def show_about(self): pass

    @StoreAction
    def toggle_sources_display(self): pass

    @StoreAction
    def toggle_show_all_lus(self): pass

    @pyqtSlot(int)
    def _tab_close(self, index):
        if self.count() > 1:
            self.removeTab(index)


class SingleTab(QWebEngineView):
    def __init__(self, tab_widget: TabWidget, url: Optional[QUrl] = None):
        super().__init__()
        self._tab_widget = tab_widget
        self.settings().setAttribute(QWebEngineSettings.JavascriptCanAccessClipboard, True)
        self.settings().setAttribute(QWebEngineSettings.ShowScrollBars, False)
        if url:
            self.load(url)
        self._rpc = JSCallReceiver(self.page())
        self._loaded = False
        self.loadFinished.connect(self.on_page_load)

    def on_page_load(self):
        self._loaded = True

    def createWindow(self, type_):
        return self._tab_widget.new_tab()
