from urls import pages
from wsgi_fw.controllers import FrontController

app = FrontController(pages)
