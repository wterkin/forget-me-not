#!/usr/bin/python
## -*- coding: utf-8 -*-

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#from datetime 
import datetime as dt

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
    fcolor = Column(String,
                    nullable=False)
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
    fname = Column(String,
                    nullable=False)
    fday = Column(Integer,
                  nullable=False)
    fmonth = Column(Integer,
                    nullable=False)    
    fyear = Column(Integer,
                   nullable=False)    
    ftype = Column(Integer, ForeignKey(CEventType.id))


    def __init__(self, pname, pdate, ptype):
        """Конструктор."""
        self.fname = pname
        self.fday = pdate.day
        self.fmonth = pdate.month
        self.fyear = pdate.year
        self.ftype = ptype
        #print("*** ", self.fname, self.fday, self.fmonth, self.fyear, self.ftype)



class CDatabase(object):
    """Класс осуществляет работу с БД."""
    def __init__(self, pdatabase_path):
        """Конструктор."""
        print("*1 ", pdatabase_path)
        self.engine = create_engine('sqlite:///'+pdatabase_path)
        self.session = sessionmaker(bind=self.engine)()
        #self.metadata = MetaData()
        Base.metadata.bind = self.engine

        #self.session.configure(bind=self.engine)

    def migrate(self):
        """Создает или изменяет БД в соответствии с описанной в классах структурой."""
        Base.metadata.create_all()
        count = self.session.query(CEventType).count()
        print("*** Count: ", count)
        if count == 0:
            #tk_rgb = "#%02x%02x%02x" % (128, 192, 200)
            print("*** insert")
            event_type = CEventType("День памяти ", "#8db0bd")
            self.session.add(event_type)
            event_type = CEventType("День рождения ", "#ecc176")
            self.session.add(event_type)
            event_type = CEventType("Памятная дата - ", "#02b6ec")
            self.session.add(event_type)
            event_type = CEventType("Напоминание: ", "#6dec04")
            self.session.add(event_type)
            self.session.commit()


    def get_event_data(self, pid):
        """Возвращает данные события в словаре."""
        #event_dict = dict()
        event_data = self.session.query(CEvent.fname,
                                        CEvent.fyear,
                                        CEvent.fmonth,
                                        CEvent.fday,
                                        CEvent.ftype).filter_by(id=pid).first()
        return (event_data.fname,
                dt.date(event_data.fyear,
                        event_data.fmonth,
                        event_data.fday),
                event_data.ftype)
    
    
    def get_events_list(self):
        """Возвращает события из базы."""
        event_name_list = []
        event_id_list = []
        queried_data = self.session.query(CEvent).order_by(CEvent.ftype, CEvent.fname)
        #print("$$$$ ",queried_data)
        for event in queried_data: 
            
            event_name_list.append(event.fname)
            event_id_list.append(event.id)
        return event_id_list, event_name_list


    def get_event_types_list(self):
        """Возвращает события из базы."""
        event_types_name_list = []
        event_types_id_list = []
        queried_data = self.session.query(CEventType).order_by(CEventType.fname)
        for event_type in queried_data: 
            
            event_types_name_list.append(event_type.fname)
            event_types_id_list.append(event_type.id)
        return event_types_id_list, event_types_name_list


    def insert_event(self, pname, pdate, ptype):
        """Добавляет новое событие в БД."""
        event = CEvent(pname, pdate, ptype)
        self.session.add(event)
        self.session.commit()


    def update_event(self, pid, pname, pdate, ptype):
        """Изменяет уже существующее событие в БД."""
        #event_data = self.session.query(CEvent.fname,
                                        #CEvent.fyear,
                                        #CEvent.fmonth,
                                        #CEvent.fday,
                                        #CEvent.ftype).filter_by(id=pid).first()
        #session.query(Customers).filter(Customers.id! = 2).
        event_data = self.session.query(CEvent).filter_by(id=pid) #.first()
        event_data.update({CEvent.fname:pname,
                           CEvent.fyear:pdate.year,
                           CEvent.fmonth:pdate.month,
                           CEvent.fday:pdate.day,
                           CEvent.ftype:ptype}, synchronize_session = False)
        #event_data.fname = pname
        #event_data.fyear = pdate.year
        #event_data.fmonth = pdate.month
        #event_data.fday = pdate.day
        #event_data.ftype = ptype
        #rows = Stat.query.filter_by(user_id = u_id).update({'user_id': 1})
        self.session.commit()
