from views import HomeView, ProductsView, ContactsView
from wsgi_fw.pages import BasePage

pages = [
    BasePage('', HomeView()),
    BasePage('products/', ProductsView()),
    BasePage('contacts/', ContactsView())
]
