class BaseView:
    def __init__(self, template, content=None):
        self.template = template
        self.content = content
        self.request = None
