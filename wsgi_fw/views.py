class BaseView:
    def __init__(self):
        self.request = None

    def get_request(self):
        if self.request and self.request.method == 'POST':
            wsgi_input = self.request.environ['wsgi.input'].read(
                int(self.request.environ['CONTENT_LENGTH']))
            wsgi_input = wsgi_input.decode('utf-8')
            wsgi_input = wsgi_input.split('&')
            wsgi_input = [w_i.split('=') for w_i in wsgi_input]
            wsgi_dict = {}
            for k, v in wsgi_input:
                wsgi_dict[k] = v
            self.post(wsgi_dict)

    def post(self, wsgi_dict):
        pass
