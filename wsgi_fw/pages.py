from dataclasses import dataclass

from wsgi_fw.views import BaseView


@dataclass
class BasePage:
    path: str
    view: BaseView
# IR Receiver Module
