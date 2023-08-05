""" This module provides a WSGI app for the Valles Web Backend"



    This module provides a WSGI app which implements the Vallex Web Backend.
    Pass it to any WSGI Server to expose it to the internet:

    Example:
    --------

    The app itself provides a simple HTTP server. The following example runs
    the app in this simple development server::

        from vallex.server.wsgi_app import app
        app.run(host='localhost', port=8080)

    In production one would probably use a server like `Gunicorn <https://gunicorn.org/>`_.

    The app provides a `REST <https://en.wikipedia.org/wiki/Representational_State_Transfer>`-like
    API. Currently only `JSON <https://www.json.org/>`_-encoded
    responses are implemented. The API is documented in the
    docstrings of the methods handling the API requests in :mod:`vallex.server.views`.
"""
import os

from pathlib import Path

from vallex import Config

from . import views
from .app_state import AppState
from .bottle_utils import WebAppFactory
from .maint import webdb_migrate
from .sql_store import SQLStore


cfg = Config()
env_db = os.environ.get('PY_VALLEX_WEB_DB', None)
if env_db:
    cfg.web_db = Path(env_db).absolute()

if not cfg.web_db.exists():
    need_migration = True
else:
    need_migration = False

store = SQLStore(cfg.web_db)

if need_migration:
    webdb_migrate(store)

state = AppState(cfg, store)

app = WebAppFactory.create_app(state)
