from abc import ABC

from wsgi_fw.constants import HTTP_404_PAGE
from wsgi_fw.decorators import debug
from wsgi_fw.exceptions import NoTemplate
from wsgi_fw.requests import RequestHandler
from wsgi_fw.utils import check_view, render


class BaseController(ABC):
    @debug
    def process_view(self, page, start_response, request):
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
        if 'template' in type(page.view).__dict__ and 'get_content' in page.view.__class__.__dict__:
            page_content = render(page.view.template, page.view.get_content())
        elif 'template' in type(page.view).__dict__ and 'content' in page.view.__class__.__dict__:
            page_content = render(page.view.template, page.view.content)
        elif 'template' in page.view.__class__.__dict__:
            page_content = render(page.view.template)
        else:
            raise NoTemplate()
        page.view.request = request
        page.view.get_request()

        return [page_content.encode()]


class FrontController(BaseController):
    def __init__(self, pages):
        self.pages = pages

    def __call__(self, environ, start_response):
        request = RequestHandler(environ)

        for page in self.pages:
            if check_view(page, request.path):
                 return self.process_view(page, start_response, request)
        else:
            start_response('404 Page Not Found', [('Content-Type', 'text/html')])

            return [HTTP_404_PAGE]


class PageController(BaseController):
    def __init__(self, page):
        self.page = page

    def __call__(self, environ, start_response):
        request = RequestHandler(environ)

        if check_view(self.page, environ['PATH_INFO']):
            return self.process_view(self.page, start_response, request)
        else:
            start_response('404 Page Not Found', [('Content-Type', 'text/html')])

            return [HTTP_404_PAGE]
