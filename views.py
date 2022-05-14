from models import Categories, Courses
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

        content = []
        for category in categories:
            category_courses = database.find('courses', category_id=category.id)
            result = {'name': category.name, 'courses': category_courses}
            content.append(result)

        return {'categories': content}


class ContactsView(BaseView):
    template = 'contacts.html'
    content = {'contacts': ['Tel.: 0782739275', 'E-Mail: support@example.com']}
    debug = True

    def post(self, wsgi_dict):
        print(wsgi_dict)


class AdminsView(BaseView):
    template = 'admins_base.html'
    debug = True


class AdminsCreateCategoryView(BaseView):
    template = 'create_category.html'
    debug = True

    def post(self, wsgi_dict):
        database = Database()
        new_category = Categories.Meta(wsgi_dict['name'])
        database.create(new_category)


class AdminsCreateCourseView(BaseView):
    template = 'create_course.html'
    debug = True

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
