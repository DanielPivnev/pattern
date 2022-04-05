from wsgi_fw.views import BaseView


home_view = BaseView('../templates/home.html', {'new': ['computers', 'smartphones']})

products_view = BaseView('../templates/products.html', {'products': ['computers', 'smartphones', 'books', 'tables']})

contacts_view = BaseView('../templates/contacts.html', {'contacts': ['Tel.: 0782739275', 'E-Mail: support@example.com']})
