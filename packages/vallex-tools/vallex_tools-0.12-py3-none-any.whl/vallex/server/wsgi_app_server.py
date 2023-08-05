import threading

import vallex.server.views

from vallex.config import Config
from vallex.server import app_state, bottle_utils, utils
from vallex.server.sql_store import SQLStore
from vallex.term import STATUS
from vallex.vendor.bottle import WSGIRefServer  # type: ignore


class AppServer:
    def __init__(self, config: Config, store: SQLStore):
        self.config = config
        self.store = store
        self.state = app_state.AppState(self.config, self.store)
        self.webapp = bottle_utils.WebAppFactory.create_app(self.state)
        self.running = False
        self.port = 8800

    @property
    def url(self):
        return 'http://localhost:'+str(self.port)+'/'

    def start(self):
        if not self.running:
            self.port = utils.find_free_port(self.port)

            # Start the server
            global server
            server = WSGIRefServer(host='localhost', port=self.port)
            self.server_thread = threading.Thread(target=server.run, args=[self.webapp])
            STATUS.start_action("Starting server")
            self.server_thread.start()
            utils.wait_for_port(self.port)
            STATUS.end_action()
            STATUS.print("Serving on", self.url)
            self.running = True

    def stop(self):
        global server
        if self.running:
            STATUS.start_action("Stopping server")
            server.srv.shutdown()
            self.server_thread.join()
            STATUS.end_action()
            self.running = False

    def restart(self):
        self.stop()
        self.start()
