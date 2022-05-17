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
