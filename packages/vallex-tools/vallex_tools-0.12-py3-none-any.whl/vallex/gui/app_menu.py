from collections import defaultdict
from typing import Callable, Dict, List, Optional, Tuple

from PyQt5.QtWidgets import QAction, QMainWindow  # type: ignore
from PyQt5.QtGui import QIcon  # type: ignore


class AppMenu:
    MENUS: Dict[str, List[Tuple[str, str, str, str, Callable]]] = defaultdict(list)

    @classmethod
    def item(cls, menu_location: str, title: str, icon: Optional[str] = None, tooltip: Optional[str] = None, shortcut: Optional[str] = None):
        def decorator(method):
            cls.MENUS[menu_location].append((title, icon, tooltip, shortcut, method))
            return method
        return decorator

    @classmethod
    def separator(cls, menu_location: str):
        cls.MENUS[menu_location].append((None, None, None, None, None))  # type: ignore

    def __init__(self, main_window: QMainWindow):
        self.menubar = main_window.menuBar()
        for top_menu, items in self.MENUS.items():
            menu = self.menubar.addMenu(top_menu)
            for title, icon, tooltip, shortcut, handler in items:
                if title is None:
                    menu.addSeparator()
                else:
                    if icon:
                        act = QAction(QIcon.fromTheme(icon), title, main_window)
                    else:
                        act = QAction(title, main_window)
                    if shortcut:
                        act.setShortcut(shortcut)
                    if tooltip:
                        act.setToolTip(tooltip)
                    act.triggered.connect(getattr(main_window, handler.__name__))
                    handler.__action__ = act  # type: ignore
                    menu.addAction(act)

    @classmethod
    def toggle_title(cls, act: QAction, title_true: str, title_false: str):
        def handler(state):
            if state:
                act.setText(title_true)
            else:
                act.setText(title_false)
        return handler
