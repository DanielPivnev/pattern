import webbrowser
from time import time
from requests import Session

from wsgi_fw.database import Database
from wsgi_fw.views import BaseView


def debug(func):
    def wrapper(*args):
        print(args)
        view = None
        for arg in args:
            if isinstance(arg, BaseView):
                view = arg
        if 'debug' in type(view).__dict__ and view.debug:
            start = time()
            response = func(*args)
            end = time()

            view_name = type(args[1].view).__name__
            full_time = round(end - start, 3)
            print(f'{view_name} - {full_time}s')

            return response
        else:
            return func(*args)
    return wrapper



