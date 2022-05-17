from wsgi_fw.views import BaseView


def post(wsgi_input):
    print(wsgi_input)


home_view = BaseView('home.html', {'new': ['computers', 'smartphones']})

products_view = BaseView('products.html', {'products': ['computers', 'smartphones', 'books', 'tables']})

contacts_view = BaseView('contacts.html', {'contacts': ['Tel.: 0782739275', 'E-Mail: support@example.com']},
                         post)
