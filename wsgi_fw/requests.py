from urllib.parse import parse_qs


class RequestHandler:
    def __init__(self, environ):
        self.environ = environ
        self.headers = {}
        self.method = environ['REQUEST_METHOD']
        self.path = environ['PATH_INFO']
        self.query_params = parse_qs(environ['QUERY_STRING'])

        for k, v in self.environ.items():
            if k.startswith('HTTP_'):
                self.headers[k[5:]] = v
