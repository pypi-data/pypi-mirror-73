def set_trace():
    from PyQt5.QtCore import pyqtRemoveInputHook  # type: ignore
    import pdb  # type: ignore
    pyqtRemoveInputHook()
    pdb.set_trace()
