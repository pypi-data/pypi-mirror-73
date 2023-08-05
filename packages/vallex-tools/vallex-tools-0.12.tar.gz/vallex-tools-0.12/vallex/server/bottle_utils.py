""" A module containing helper methods for the bottle.py framework.




    The module abstracts several common patterns to allow simpler specification
    of the WSGI app. It defines the following classes:

        - :class:`Error`, :class:`BadRequest`, :class:`NotFound`,
          :class:`Forbidden` exceptions representing a HTTP error
        - :func:`compress_handler` a wrapper which compresses the response data
        - :func:`json_handler` a wrapper which converts the response object into JSON
        - :func:`inject_arg` a wrapper which injects a keyword argument into the wrapped method
        - :class:`Environment` a named tuple which stores the bottle, request, response and AppState objects
        - :class:`WebAppFactory` a class which is used to register routes and create wsgi apps
"""
import os
import time
import zlib

from functools import wraps
from typing import Callable, List, NamedTuple, Tuple

from vallex.vendor import bottle
from vallex.json_utils import dumps

from .app_state import AppState


class Error(Exception):
    """
        An exception which, in addition to a message, holds an appropriate HTTP status code.

        Attributes:
            _msg:       An error message
            _status:    A HTTP Status code

    """

    BAD_REQUEST = 400
    FORBIDDEN = 403
    NOT_FOUND = 404

    def __init__(self, status: int, *message):
        msg = ' '.join([str(arg) for arg in message])
        super().__init__(msg)
        self._status: int = status
        self._message: str = msg

    def __json__(self, **opts):
        return {'error': self._message, 'status_code': self._status}

    @classmethod
    def catch_error(cls, func, handle_all_exceptions=False):
        """
            Wraps an url-handler method so that any Error exceptions raised by the handler
            are caught and an appropriate error response is returned.

            Optionally if `handle_all_exceptions` is ``True``, all exceptions are caught
            and for exceptions which are not instances of the Error class, a
            '500 Internal Server Error' status is set and the exception is converted to
            ``str`` and returned in as the ``error`` attribute of the response object.
        """
        if handle_all_exceptions:
            @wraps(func)
            def wrapped(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Error as err:
                    bottle.response.content_type = 'application/json'
                    bottle.response.status = str(err._status)+' '+err._message
                    return dumps(err)
                except Exception as ex:
                    bottle.response.content_type = 'application/json'
                    bottle.response.status = '500 Internal Server Error'
                    return dumps({'error': str(ex), 'status_code': 500})
        else:
            @wraps(func)
            def wrapped(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Error as err:
                    bottle.response.content_type = 'application/json'
                    bottle.response.status = str(err._status)+' '+err._message
                    return dumps(err)
        return wrapped


class BadRequest(Error):
    """A special case of Error, returning the BAD REQUEST status code"""

    def __init__(self, *message):
        super().__init__(self.BAD_REQUEST, *message)


class NotFound(Error):
    """A special case of Error, returning the NOT FOUND status code"""

    def __init__(self, *message):
        super().__init__(self.NOT_FOUND, *message)


class Forbidden(Error):
    """A special case of Error, returning the FORBIDDEN status code"""

    def __init__(self, *message):
        super().__init__(self.FORBIDDEN, *message)


def compress_handler(func: Callable) -> Callable:
    """
        Wraps an url-handler method so that the result is automatically compressed
        and appropriate headers are added to the response.
    """
    @wraps(func)
    def wrapped(*args, **kwargs):
        out = zlib.compress(bytes(func(*args, **kwargs), encoding='utf-8'))
        bottle.response.add_header("Content-Encoding", "deflate")
        return out
    return wrapped


def json_handler(func: Callable) -> Callable:
    """
        Wraps an url-handler method so that the result is automatically converted
        into JSON provided it is not a str/bytes instance.
    """
    @wraps(func)
    def wrapped(*args, **kwargs):
        ret = func(*args, **kwargs)
        if ret and not isinstance(ret, (str, bytes, bottle.HTTPResponse)):
            bottle.response.content_type = 'application/json'
            return dumps(ret, include_dynamic_attrs=True)
        return ret
    return wrapped


def timestamp_handler(func: Callable) -> Callable:
    """
        Wraps an url-handler which adds a `ts` key to the resulting JSON object
        with the timestamp corresponding to the time the request was received.
    """
    @wraps(func)
    def wrapped(*args, **kwargs):
        ts = time.time()
        ret = func(*args, **kwargs)
        if isinstance(ret, dict):
            ret['ts'] = ts
        return ret
    return wrapped


def inject_arg(func: Callable, arg_name: str, arg_value) -> Callable:
    """
        Wraps the function funct and injects `arg_value`  as its `arg_name`
        keyword argument
    """
    @wraps(func)
    def wrapped(*args, **kwargs):
        kwargs.update({arg_name: arg_value})
        return func(*args, **kwargs)
    return wrapped


class Environment(NamedTuple):
    """
        Stores several objects useful to route handlers

        Attributes:
            app:        the Bottle app
            request:    the request object
            response:   the response object
            state:      an AppState object holding application state
                        shared across requests
    """
    app: bottle.Bottle  # type: ignore
    request: bottle.Request  # type: ignore
    response: bottle.Response  # type: ignore
    state: AppState


def prepare_db(func: Callable, env: Environment) -> Callable:
    """
        Wraps an url-handler method into code that first ensures that there
        is an open connection to the db and, after finishing, ensures that
        the connection is cleaned up, if necessary.
    """
    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            env.state.store.ensure_connection()
            return func(*args, **kwargs)
        finally:
            env.state.store.connection_can_close()
    return wrapped


class WebAppFactory:
    """
        A class which is used to register route handlers and create
        wsgi app instances

        Attributes:
            _ROUTES:   A list of route handlers, n instance of the bottle.app
    """

    _ROUTES: List[Tuple[str, str, Callable, bool]] = []

    @classmethod
    def create_app(cls, state=None):
        """
            Creates a bottle WSGI app, applies the routes registered via :meth:`WebAppFactory.route` method
            to it, injecting the state into the environment (optionally) passed to the route handlers.
        """
        app = bottle.app()
        cls.apply_routes(app, state)
        return app

    @classmethod
    def apply_routes(cls, app, state):
        """
            Applies the routes registered via :meth:`WebAppFactory.route` method to the
            application `app`, injecting `state` into the environment given to the routes.
        """
        env = Environment(app=app, request=bottle.request, response=bottle.response, state=state)
        for url, method, handler, inject_env in cls._ROUTES:
            if inject_env:
                handler = inject_arg(handler, 'env', env)
            handler = prepare_db(handler, env)
            app.route(url, method)(handler)

    @classmethod
    def route(cls, url: str, method: str, CORS: bool = False, compress=False, inject_env=True, add_timestamp=False):
        """
            A decorator which defines the decorated method as a handler for requests to `url`

            If CORS is True, it additionally automatically adds a method to handle OPTIONS requests
            for the given `url` returning an empty response with appropriately set headers to allow
            CORS. Moreover, the decorated method is wrapped in a method which adds a ``Access-Control-Allow-Origin: *``
            header to the response.

            If compress is True the result returned by the decorated method is automatically compressed
            and appropriate Content-Encoding header is added to the response.

            If inject_env is true, the method will automatically receive an ``env`` keyword argument
            which is a namedtuple :class:`Environment` containing, amongst others, the request and
            response objects, the bottle app and application state passed to the :func:`create_app`
            function when creating the app.
        """

        # Add OPTIONS method for the route
        if CORS:
            def opts(*_, **_kw):
                bottle.response.add_header('Access-Control-Allow-Origin', '*')
                bottle.response.add_header('Access-Control-Allow-Methods', method)
                bottle.response.add_header('Access-Control-Allow-Headers', 'Content-Type, Access-Control-Allow-Headers, X-Requested-With')
            cls._ROUTES.append((url, 'OPTIONS', opts, False))

        def wrapper(func):
            # Add Access-Control header for CORS enabled routes
            if CORS:
                @wraps(func)
                def handler(*args, **kwargs):
                    bottle.response.add_header('Access-Control-Allow-Origin', '*')
                    return func(*args, **kwargs)
            else:
                handler = func

            # Add timestamps, if requested
            if add_timestamp:
                handler = timestamp_handler(handler)

            # Automatically convert non-str/non-byte responses to JSON
            handler = json_handler(handler)

            # Optionally compress output
            if compress:
                handler = compress_handler(handler)

            # Catch Error exeptions and convert them to appropriate HTTP Status Codes
            handler = Error.catch_error(handler, handle_all_exceptions=os.environ.get('_PYTEST_RUN', ''))

            cls._ROUTES.append((url, method, handler, inject_env))
            return handler
        return wrapper
