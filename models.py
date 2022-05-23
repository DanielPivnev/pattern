from wsgi_fw.database import String, Integer, Float
from wsgi_fw.database import BaseModel


class Courses(BaseModel):
    table_name = 'courses'
    _name_ = String
    _category_id_ = Integer
    _price_ = Float
    _c_type_ = String
    _first_name_ = String
    _last_name_ = String

    class Meta:
        def __init__(self, name, category_id, price, first_name, last_name, c_type):
            self.id = None
            self.name = name
            self.category_id = category_id
            self.price = price
            self.first_name = first_name
            self.last_name = last_name
            self.c_type = c_type


class Categories(BaseModel):
    table_name = 'categories'
    _name_ = String

    class Meta:
        def __init__(self, name):
            self.id = None
            self.name = name


class UsersAtCourses(BaseModel):
    table_name = 'users_at_courses'
    _course_id_ = Integer
    _user_id_ = Integer

    class Meta:
        def __init__(self, course_id, user_id):
            self.id = None
            self.course_id = course_id
            self.user_id = user_id


class Users(BaseModel):
    table_name = 'users'
    _email_ = String
    _address_ = String
    _city_ = String
    _country_ = String
    _password_ = String

    class Meta:
        def __init__(self, email, address, city, country, password):
            self.id = None
            self.email = email
            self.address = address
            self.city = city
            self.country = country
            self.password = password


class Admins(BaseModel):
    table_name = 'admins'
    _email_ = String
    _full_name_ = String
    _password__ = String
    _wage_ = Float
    _password_ = String

    class Meta:
        def __init__(self, email, full_name, wage, password):
            self.id = None
            self.email = email
            self.full_name = full_name
            self.wage = wage
            self.password = password
