from pprint import pprint


class BaseView:
    def __init__(self, template, content=None, post_method=None):
        self.template = template
        self.content = content
        self.request = None
        self.post_method = post_method

    def get_request(self):
        if self.request and self.request.method == 'POST':
            self.post_method(self.request.environ['wsgi.input'].read(int(self.request.environ['CONTENT_LENGTH'])))
