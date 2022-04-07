from wsgi_fw.constants import HTTP_404_PAGE
from wsgi_fw.requests import RequestHandler
from wsgi_fw.utils import check_view, render


class FrontController:
    def __init__(self, pages):
        self.pages = pages

    def __call__(self, environ, start_response):
        request = RequestHandler(environ)

        for page in self.pages:
            if check_view(page, request.path):
                start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
                page_content = render(page.view.template,
                                      page.view.content) if page.view.content else page.view.template
                page.view.request = request
                page.view.get_request()

                return [page_content.encode()]
        else:
            start_response('404 Page Not Found', [('Content-Type', 'text/html')])

            return [HTTP_404_PAGE]


class PageController:
    def __init__(self, page):
        self.page = page

    def __call__(self, environ, start_response):
        if check_view(self.page, environ['PATH_INFO']):
            start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
            page_content = self.page.view.template

            return [page_content.encode()]
        else:
            start_response('404 Page Not Found', [('Content-Type', 'text/html')])

            return [HTTP_404_PAGE]
