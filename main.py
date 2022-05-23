from models import Courses, Categories, Users, Admins, UsersAtCourses
from urls import pages
from wsgi_fw.controllers import FrontController
from wsgi_fw.database import Database


database = Database('courses_uni')
database.create_tables(Courses, Categories, UsersAtCourses, Users, Admins)

app = FrontController(pages)
