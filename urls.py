from views import home_view, contacts_view, products_view
from wsgi_fw.pages import BasePage

pages = [
    BasePage('', home_view),
    BasePage('products/', products_view),
    BasePage('contacts/', contacts_view)
]
