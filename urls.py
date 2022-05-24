from views import HomeView, ProductsView, ContactsView, AdminsView, AdminsCreateCourseView, AdminsCreateCategoryView, \
    RegistrationView, LoginView, LogoutView
from wsgi_fw.pages import BasePage

pages = [
    BasePage('', HomeView()),
    BasePage('products/', ProductsView()),
    BasePage('contacts/', ContactsView()),
    BasePage('admins/', AdminsView()),
    BasePage('admins/create/category/', AdminsCreateCategoryView()),
    BasePage('admins/create/course/', AdminsCreateCourseView()),
    BasePage('registration/', RegistrationView()),
    BasePage('login/', LoginView()),
    BasePage('logout/', LogoutView())
]
