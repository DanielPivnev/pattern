import sqlite3
import threading
from abc import ABC

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, Float
from sqlalchemy.orm import mapper, sessionmaker, scoped_session

from wsgi_fw.singeltons import Singleton


class Database(metaclass=Singleton):
    def __init__(self, name='database'):
        self.ENGINE = create_engine(f'sqlite:///{name}.sqlite', echo=False, pool_recycle=7200, connect_args={
            'check_same_thread': False})
        self.session = scoped_session(sessionmaker(bind=self.ENGINE))
        self.tables = {}

        self.session.commit()

        self.connection = sqlite3.connect(name)
        self.cursor = self.connection.cursor()

    def create_tables(self, *args):
        for item_cls in args:
            metadata = MetaData()
            columns = [Column(name, data_type) for name, data_type in item_cls.get_columns(item_cls)]
            table = Table(item_cls.table_name, metadata,
                          Column('id', Integer, primary_key=True),
                          *columns)

            metadata.create_all(self.ENGINE)
            mapper(item_cls.Meta, table)
            self.tables[item_cls.table_name] = (table, item_cls.Meta)

            self.session.commit()

    def create(self, item):
        self.session.add(item)
        self.session.commit()

    def create_own_orm(self, table_name, *args):
        statement = "INSERT INTO PERSON (FIRSTNAME, LASTNAME) VALUES ("
        for arg in args:
            statement += f'{arg}, '
        statement = statement[:-2] + ')'
        self.cursor.execute(statement, (table_name,))
        try:
            self.connection.commit()
        except Exception as e:
            print(e)

    def delete(self, table_name, item_id):
        table, item_cls = self.tables[table_name]
        self.session.query(table).filter_by(id=item_id).delete()
        self.session.commit()

    def delete_own_orm(self, table_name, item_id):
        statement = "DELETE FROM ? WHERE id=?"
        self.cursor.execute(statement, (table_name, item_id))
        try:
            self.connection.commit()
        except Exception as e:
            print(e)

    def find(self, table_name, **kwargs):
        table, item_cls = self.tables[table_name]
        response = self.session.query(item_cls).filter_by(**kwargs)

        return response.all()

    def find_own_orm(self, table_name, **kwargs):
        statement = "SELECT * FROM ? WHERE"
        for key, value in kwargs:
            statement += f' {key}={value} AND'
        statement = statement[:-4]
        self.cursor.execute(statement, (table_name,))
        result = self.cursor.fetchone()

        return result

    def all(self, table_name):
        return self.session.query(self.tables[table_name][1]).all()

    def update(self):
        self.session.commit()

    def update_own_orm(self, table_name, item_id, **kwargs):
        statement = "UPDATE ? SET"
        for k, v in kwargs:
            statement += f' {k}={v}'
        statement += ' WHERE id=?'
        self.cursor.execute(statement, (table_name, item_id))
        try:
            self.connection.commit()
        except Exception as e:
            print(e)


class MapperRegistry:
    @staticmethod
    def get_mapper():
        return Database()


class UnitOfWork:
    current = threading.local()

    def __init__(self):
        self.new_objects = []
        self.dirty_objects = []
        self.removed_objects = []

    def register_new(self, table_name, *args):
        self.new_objects.append({'name': table_name, 'values': args})

    def register_dirty(self, table_name, item_id, **kwargs):
        self.dirty_objects.append({'name': table_name, 'id': item_id, 'values': kwargs})

    def register_removed(self, table_name, item_id):
        self.removed_objects.append({'name': table_name, 'id': item_id})

    def commit(self):
        self.insert_new()
        self.update_dirty()
        self.delete_removed()

    def insert_new(self):
        for obj in self.new_objects:
            MapperRegistry.get_mapper().create_own_orm(obj.name, *obj.values)

    def update_dirty(self):
        for obj in self.dirty_objects:
            MapperRegistry.get_mapper().update_own_orm(obj.name, obj.id, **obj.values)

    def delete_removed(self):
        for obj in self.removed_objects:
            MapperRegistry.get_mapper().delete_own_orm(obj.name, obj.id)

    @staticmethod
    def new_current():
        __class__.set_current(UnitOfWork())


    @classmethod
    def set_current(cls, unit_of_work):
        cls.current.unit_of_work = unit_of_work


    @classmethod
    def get_current(cls):
        return cls.current.unit_of_work


class BaseModel(ABC):
    def get_columns(self):
        columns = []
        for k in self.__dict__.keys():
            if k[0] == '_' and k[1] != '_' and k[-1] == '_' and k[-2] != '_':
                data_type = self.__dict__[k]
                columns.append((k[1:-1], data_type))

        return columns
