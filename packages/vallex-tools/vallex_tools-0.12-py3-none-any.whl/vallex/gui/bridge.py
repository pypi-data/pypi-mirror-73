from PyQt5.QtCore import pyqtSignal, pyqtSlot, QFile, QIODevice, QObject  # type: ignore
from PyQt5.QtWebChannel import QWebChannel  # type: ignore
from PyQt5.QtWebEngineWidgets import QWebEngineScript  # type: ignore

Q_WEBCHANNEL_FILE = QFile(':/qtwebchannel/qwebchannel.js')
Q_WEBCHANNEL_FILE.open(QIODevice.ReadOnly)
Q_WEBCHANNEL_SRC = bytes(Q_WEBCHANNEL_FILE.readAll()).decode('utf-8')
Q_WEBCHANNEL_SCRIPT = QWebEngineScript()
Q_WEBCHANNEL_SCRIPT.setSourceCode(Q_WEBCHANNEL_SRC + """
    new QWebChannel(qt.webChannelTransport, function (channel) {
        window.pyqt_app = channel.objects.pyqt_app
    })
""")
Q_WEBCHANNEL_SCRIPT.setName('qwebchannel.js')
Q_WEBCHANNEL_SCRIPT.setWorldId(QWebEngineScript.MainWorld)
Q_WEBCHANNEL_SCRIPT.setInjectionPoint(QWebEngineScript.DocumentReady)
Q_WEBCHANNEL_SCRIPT.setRunsOnSubFrames(True)


class JSCallReceiver(QObject):

    message_result = pyqtSignal(str, str)

    @pyqtSlot(str, str)
    def message_action(self, msg_id, action):
        self.message_result.emit(msg_id, action)

    def __init__(self, page):
        super().__init__()
        self._page = page
        self.channel = QWebChannel()
        self.channel.registerObject('pyqt_app', self)
        self._page.setWebChannel(self.channel)
        self._page.scripts().insert(Q_WEBCHANNEL_SCRIPT)
