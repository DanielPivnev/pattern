from wsgi_fw.views import BaseView


class HomeView(BaseView):
    template = 'home.html'
    content = {'new': ['computers', 'smartphones']}


class ProductsView(BaseView):
    template = 'products.html'
    content = {'products': ['computers', 'smartphones', 'books', 'tables']}


class ContactsView(BaseView):
    template = 'contacts.html'
    content = {'contacts': ['Tel.: 0782739275', 'E-Mail: support@example.com']}

    def post(self, wsgi_input):
        print(wsgi_input)
