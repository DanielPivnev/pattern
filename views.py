from models import Categories, Courses, Users, Admins, UsersAtCourses
from wsgi_fw.constants import STUDENT, ADMIN
from wsgi_fw.database import Database
from wsgi_fw.views import BaseView


class HomeView(BaseView):
    template = 'home.html'
    content = {'new': ['computers', 'smartphones']}
    debug = True


class ProductsView(BaseView):
    template = 'products.html'
    debug = True

    def get_content(self):
        database = Database()
        categories = database.all('categories')

        content, active = [], []
        for category in categories:
            category_courses = database.find('courses', category_id=category.id)
            result = {'name': category.name, 'courses': category_courses}
            content.append(result)

        return {'categories': content, 'active': active}

    def post(self, wsgi_dict):
        if wsgi_dict and self.is_student():
            database = Database()
            print(self.get_user_id())
            new_abo = UsersAtCourses.Meta(wsgi_dict['id'], self.get_user_id())
            database.create(new_abo)


class ContactsView(BaseView):
    template = 'contacts.html'
    content = {'contacts': ['Tel.: 0782739275', 'E-Mail: support@example.com']}
    debug = True

    def post(self, wsgi_dict):
        print(wsgi_dict)


class AdminsView(BaseView):
    template = 'admins_base.html'
    debug = True
    login = 'please_login.html'


class AdminsCreateCategoryView(BaseView):
    template = 'create_category.html'
    debug = True
    login = 'please_login.html'

    def post(self, wsgi_dict):
        database = Database()
        new_category = Categories.Meta(wsgi_dict['name'])
        database.create(new_category)


class AdminsCreateCourseView(BaseView):
    template = 'create_course.html'
    debug = True
    login = 'please_login.html'

    def post(self, wsgi_dict):
        if wsgi_dict:
            database = Database()
            new_course = Courses.Meta(wsgi_dict['cn'], int(wsgi_dict['category']), int(wsgi_dict['price']),
                                      wsgi_dict['fn'], wsgi_dict['ln'], wsgi_dict['type'])
            database.create(new_course)

    def get_content(self):
        database = Database()
        categories = database.all('categories')

        return {'categories': categories}


class RegistrationView(BaseView):
    template = 'registration.html'
    debug = True

    def post(self, wsgi_dict):
        if wsgi_dict:
            database = Database()
            if not len(database.find(Users.table_name, email=wsgi_dict['email'])) \
                    and wsgi_dict['password1'] == wsgi_dict['password2']:
                new_users = Users.Meta(wsgi_dict['email'], wsgi_dict['address'], wsgi_dict['city'],
                                       wsgi_dict['country'], wsgi_dict['password1'])
                database.create(new_users)

                self.auth(STUDENT, database.find(Users.table_name, email=wsgi_dict['email'])[0])


class LoginView(BaseView):
    template = 'login.html'
    debug = True

    def post(self, wsgi_dict):
        print(wsgi_dict)
        if wsgi_dict:
            database = Database()
            user, admin = database.find(Users.table_name, email=wsgi_dict['email']), database.find(Admins.table_name,
                                                                                                   email=wsgi_dict[
                                                                                                       'email'])

            if len(user) and user[0].password == wsgi_dict['password']:
                self.auth(STUDENT, user[0])
            elif len(admin) and admin[0].password == wsgi_dict['password']:
                self.auth(ADMIN, user[0])


