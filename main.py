from models import Courses, Categories
from urls import pages
from views import AdminsCreateCourseView
from wsgi_fw.controllers import FrontController
from wsgi_fw.database import Database

database = Database('courses_uni')
database.create_tables(Courses, Categories)

AdminsCreateCourseView().post({})

app = FrontController(pages)
