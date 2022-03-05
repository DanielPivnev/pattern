from views import home_view, contacts_view, products_view

pages = [
    {'path': '', 'view': home_view},
    {'path': 'products/', 'view': products_view},
    {'path': 'contacts/', 'view': contacts_view}
]
