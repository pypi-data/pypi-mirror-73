from functools import partial
from typing import Callable, Dict, List, Optional

from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, Qt, QTimer  # type: ignore
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QProgressBar, QPushButton, QStatusBar, QWidget  # type: ignore

from vallex.term import COLOR_ERROR, COLOR_OK


class Status(QWidget):

    @pyqtSlot(str, list, dict)
    def _rpc_handler(self, meth_name, args, kwargs):
        meth = getattr(self, meth_name)
        meth(*args, **kwargs)

    def __init__(self, status_bar: QStatusBar):
        super().__init__()
        self._bar = status_bar
        self._msg = QLabel(self)
        self._progress = QProgressBar(self)
        self._progress.setRange(0, 100)
        self._progress.setMaximumHeight(7)
        self._progress.setFormat("")
        self._bar.addWidget(self._msg)
        self._progress_len = 100
        self._bar.hide()
        self._lead_text = ''
        self._need_clearing = False
        self._action_buttons: List[QPushButton] = []

    def show_message(self, message: str, actions: Optional[Dict[str, Callable]] = None, msg_type: str = 'info'):
        """
            Shows a notification `message` to the user in the status bar. If actions are specified,
            the notification will have a button for each item in action. The item is a pair (ButtonLabel, Action),
            where action is either None or a slot.
        """
        self._clear_message()
        if not actions:
            self.print(message, _permanent=True)
            return
        self.print(message, _permanent=True)

        def handler(h):
            self._clear_message()
            if h:
                h()

        for act_title, act_handler in actions.items():
            btn = QPushButton(self)
            if act_handler:
                btn.clicked.connect(partial(handler, act_handler))
            else:
                btn.clicked.connect(self._clear_message)
            btn.setText(act_title)
            self._bar.addPermanentWidget(btn)
            self._action_buttons.append(btn)

    def _clear_message(self):
        self._msg.setText('')
        for btn in self._action_buttons:
            self._bar.removeWidget(btn)
        self._bar.hide()
        self._action_buttons = []

    def print(self, *args, **kwargs):
        sep = kwargs.get('sep', ' ')
        msg = sep.join([str(a) for a in args])
        self._bar.show()
        self._msg.setText(msg)
        if not '_permanent' in kwargs:
            self._need_clearing = True
            QTimer.singleShot(2000, self.clear)
        else:
            self._need_clearing = False

    def start_action(self, *heading):
        """
        Starts a new statusline, printing out heading followed by a semicolon and empty status.
        """
        self._lead_text = ' '.join([str(h) for h in heading])+':'
        self.print(self._lead_text, _permanent=True)

    def end_action(self, ok=True, message=None, preserve_status=False):
        """
        If no message is provided, the status is updated with a green ``OK`` if (`ok` is ``True``) or a
        red ``ERROR`` (if `ok` is ``False``). If a message is provided, the status is updated with this message
        instead. If preserve_status is True, the status is not updated (i.e. the last status update
        remains). Finally a new line is started.

        """
        if not preserve_status:
            mlen = 0
            if message:
                message = '('+message+') '
            else:
                message = ''
            if ok:
                result_text = message + (COLOR_OK | 'OK')
            else:
                result_text = message + (COLOR_ERROR | 'ERROR')
            self.update(result_text, clip=False)

    def update(self, *args, finish=False, clip=True):
        """
            Updates the current status (i.e. deletes the old status and replaces it with the new status).
            Status is composed by joining the stringified arguments (similar to how print works)
        """
        out_str = ' '.join([str(x) for x in args]).strip('\n')
        if finish:
            self.print(self._lead_text, *args)
        else:
            self.print(self._lead_text, *args, _permanent=True)

    @pyqtSlot(float, str)
    def progress_update(self, fraction, message):
        self.update(message)
        self._progress.setValue(int(fraction*100))

    @pyqtSlot(float, str)
    def progress_done(self, message=''):
        self.end_action()
        self._bar.removeWidget(self._progress)
        self._bar.hide()

    @pyqtSlot(str, int)
    def progress_start(self, title='', width=20):
        self._bar.addPermanentWidget(self._progress)
        self._progress.show()
        self.start_action(title)
        self._bar.show()

    @pyqtSlot()
    def clear(self, force=False):
        if self._need_clearing or force:
            self._msg.setText('')
            self._bar.hide()

    @pyqtSlot(float, str)
    def _update_handler(self, fraction, message):
        self._progress.setValue(int(self._progress_len*fraction))


class ProxyProgressBar:
    def __init__(self, status):
        self._status = status

    def update(self, fraction, message): self._status._rpc.emit('progress_update', [fraction, message], {})
    def done(self, message: str = ''): self._status._rpc.emit('progress_done', [message], {})


class StatusProxy(QObject):
    _rpc = pyqtSignal(str, list, dict)

    def __init__(self, status: Status):
        super().__init__()
        self._rpc.connect(status._rpc_handler)

    def progress_bar(self, title, width=20):
        self._rpc.emit('progress_start', [title, width], {})
        return ProxyProgressBar(self)

    def print(self, *args, **kwargs): self._rpc.emit('print', list(args), kwargs)
    def start_action(self, *args, **kwargs): self._rpc.emit('start_action', list(args), kwargs)
    def end_action(self, *args, **kwargs): self._rpc.emit('end_action', list(args), kwargs)
    def update(self, *args, **kwargs): self._rpc.emit('update', list(args), kwargs)
