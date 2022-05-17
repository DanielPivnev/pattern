class BaseView:
    def __init__(self):
        self.request = None

    def get_request(self):
        if self.request and self.request.method == 'POST':
            wsgi_input = self.request.environ['wsgi.input'].read(
                int(self.request.environ['CONTENT_LENGTH']))
            self.post(wsgi_input)

    def post(self, wsgi_input):
        pass
