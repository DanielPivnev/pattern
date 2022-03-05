from controllers.render import render


def home_view():
    return render('../templates/home.html', new=['computers', 'smartphones'])


def products_view():
    return render('../templates/products.html', products=['computers', 'smartphones', 'books', 'tables'])


def contacts_view():
    return render('../templates/contacts.html', contacts=['Tel.: 0782739275', 'E-Mail: support@example.com'])
