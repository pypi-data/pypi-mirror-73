import inspect

from functools import wraps
from typing import List

from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, QThread  # type: ignore

from vallex.term import STATUS


class WrapQObject(QObject):
    def __init__(self, obj):
        super().__init__()
        self.obj = obj

        methods = [m for m in dir(obj) if not m.startswith('_') and hasattr(getattr(obj, m), '__call__')]

        class Proxy(QObject):
            _rpc = pyqtSignal(str, list, dict)
            _methods = {}

            def __getattr__(self, name):
                if name in self._methods:
                    return self._methods[name]
                if name in methods:
                    def meth(*args, **kwargs):
                        self._rpc.emit(name, list(args), dict(kwargs))
                    self._methods[name] = meth
                    return meth
                raise AttributeError

        self.proxy = Proxy()
        self.proxy._rpc.connect(self._rpc_handler)

    @pyqtSlot(str, list, dict)
    def _rpc_handler(self, meth, args, kwargs):
        meth = getattr(self.obj, meth)
        meth(*args, **kwargs)


TASKS: List[QThread] = []


def BackgroundTask(method):

    @wraps(method)
    def decorated(*args, **kwargs):
        ret_type = inspect.signature(method).return_annotation
        if ret_type is None or ret_type is inspect._empty:
            signal_signature = []
        else:
            signal_signature = [ret_type]

        class Task(QThread):
            done = pyqtSignal(*signal_signature)
            failed = pyqtSignal(Exception)

            def run(self):
                try:
                    ret = method(*args, **kwargs)
                    if signal_signature and isinstance(ret, signal_signature[0]):
                        self.done.emit(ret)
                    elif ret:
                        STATUS.print("Invalid return value", ret, "expecting return of type", signal_signature[0] if signal_signature else None)
                    else:
                        self.done.emit()
                except Exception as ex:
                    self.failed.emit(ex)
                finally:
                    TASKS.remove(self)

        task = Task()
        TASKS.append(task)
        return task
    return decorated
