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

    def delete(self, item_id, table_name):
        table, item_cls = self.tables[table_name]
        self.session.query(table).filter_by(id=item_id).delete()
        self.session.commit()

    def find(self, table_name, **kwargs):
        table, item_cls = self.tables[table_name]
        response = self.session.query(item_cls).filter_by(**kwargs)

        return response.all()

    def all(self, table_name):
        return self.session.query(self.tables[table_name][1]).all()

    def update(self):
        self.session.commit()


class BaseModel(ABC):
    def get_columns(self):
        columns = []
        for k in self.__dict__.keys():
            if k[0] == '_' and k[1] != '_' and k[-1] == '_' and k[-2] != '_':
                data_type = self.__dict__[k]
                columns.append((k[1:-1], data_type))

        return columns
