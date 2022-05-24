from selenium import webdriver
import webbrowser
from abc import ABC
from pprint import pprint

from requests import Session

from wsgi_fw.constants import HTTP_404_PAGE, ADMIN
from wsgi_fw.decorators import debug
from wsgi_fw.exceptions import NoTemplate
from wsgi_fw.memonto import AuthorisationMemomto
from wsgi_fw.requests_fw import RequestHandler
from wsgi_fw.utils import check_view, render


class Controller(ABC):
    def notify(self, u_id):
        for page in self.pages:
            page.view.update(self.authorisation, u_id)


class FrontController(Controller):
    def __init__(self, pages):
        self.pages = pages
        self.authorisation = AuthorisationMemomto()
        self.connect_views()

    def __call__(self, environ, start_response):
        request = RequestHandler(environ)

        for page in self.pages:
            if check_view(page, request.path):
                print(f'{page.view} - {self.authorisation.get_state()}')
                return self.process_view(page, start_response, request)
        else:
            start_response('404 Page Not Found', [('Content-Type', 'text/html')])

            return [HTTP_404_PAGE]

    def connect_views(self):
        for page in self.pages:
            page.view.set_controller(self)

    def auth(self, state, u_id):
        self.authorisation.set_state(state)
        self.notify(u_id)

    def logout(self):
        self.authorisation.set_state(None)
        self.notify(None)

    @debug
    def process_view(self, page, start_response, request):
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
        if 'login' not in type(page.view).__dict__ or (
                'login' in type(page.view).__dict__ and self.authorisation.get_state() == ADMIN):
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
        else:
            return [render(type(page.view).login).encode()]


class PageController:
    def __init__(self, page):
        self.page = page

    def __call__(self, environ, start_response):
        request = RequestHandler(environ)
        self.env = environ

        if check_view(self.page, environ['PATH_INFO']):
            return self.process_view(self.page, start_response, request)
        else:
            start_response('404 Page Not Found', [('Content-Type', 'text/html')])

            return [HTTP_404_PAGE]

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
