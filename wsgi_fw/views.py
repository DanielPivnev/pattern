from pprint import pprint


class BaseView:
    content = None
    request = None

    def get_request(self):
        if self.__class__.request and self.__class__.request.method == 'POST':
            wsgi_input = self.__class__.request.environ['wsgi.input'].read(
                int(self.__class__.request.environ['CONTENT_LENGTH']))
            self.post(wsgi_input)

    def post(self, wsgi_input):
        pass
