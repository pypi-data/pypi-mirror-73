import io
import sys

from .razorbird import run_tokio


class Server:

    def __init__(self, app):
        self._app = self._wsgi_wrapper(app)

    def _wsgi_wrapper(self, app):
        wsgi_boilerplate = (
            ('REMOTE_ADDR', '127.0.0.1'),
            ('SCRIPT_NAME', ''),
            ('SERVER_NAME', '127.0.0.1'),
            ('SERVER_PORT', 8000),
            ('SERVER_SOFTWARE', 'razorbird/0.2.0'),
            ('wsgi.errors', sys.stderr),
            ('wsgi.multiprocess', False),
            ('wsgi.multithread', False),
            ('wsgi.run_once', False),
            ('wsgi.url_scheme', 'http'),
            ('wsgi.version', (1, 0)),
        )

        def handler(environ, headers, data):
            def start_response(status, response_headers, exc_info=None):
                result.extend((status, response_headers))

            environ.update(wsgi_boilerplate)
            environ.update(headers)
            environ['wsgi.input'] = io.BytesIO(data)

            result = []
            resp = app(environ, start_response)
            result.append(b''.join(resp))

            return result

        return handler

    def run(self):
        run_tokio(self._app)
