#!/usr/bin/python
## -*- coding: utf-8 -*-

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class CEventType(Base):
    __tablename__ = 'tbl_types'
    id = Column(Integer,
                autoincrement=True,
                nullable=False,
                primary_key=True,
                unique=True)
    fname = Column(String,
                    nullable=False,
                    unique=True)
    fcolor = Column(Integer)
    fstatus = Column(Integer,
                        nullable=False)
    def __init__(self, pname, pcolor):
        
        self.fname = pname
        self.fcolor = pcolor
        self.fstatus = 1
    
    def __repr__(self):
        
        return f"ID:{self.id}, Name:{self.fname}, Color:{self.fcolor}"
    
class CEvent(Base):
    __tablename__ = 'tbl_events'    
    id = Column(Integer,
                autoincrement=True,
                nullable=False,
                primary_key=True,
                unique=True)
    fday = Column(Integer,
                  nullable=False)
    fmonth = Column(Integer,
                    nullable=False)    
    fyear = Column(Integer,
                   nullable=False)    
    ftype = Column(Integer, ForeignKey(CEventType.id))


class CDatabase(object):
    """Класс осуществляет работу с БД."""
    def __init__(self, pdatabase_path):
        """Конструктор."""
        print("*1 ", pdatabase_path)
        self.engine = create_engine('sqlite://'+pdatabase_path)
        self.session = sessionmaker(bind=self.engine)
        #self.metadata = MetaData()
        Base.metadata.bind = self.engine

        #self.session.configure(bind=self.engine)

    def migrate(self):
        """Создает или изменяет БД в соответствии с описанной в классах структурой."""
        Base.metadata.create_all()

