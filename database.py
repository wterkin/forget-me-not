#!/usr/bin/python
## -*- coding: utf-8 -*-

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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
        
        return f"""ID:{self.id},
                   Name:{self.fname},
                   Color:{self.fcolor},
                   Status:{self.fstatus}"""

class CPeriod(Base):
    __tablename__ = 'tbl_periods'
    id = Column(Integer,
                autoincrement=True,
                nullable=False,
                primary_key=True,
                unique=True)
    ffreq = Column(Integer,
                   nullable=False)
    fstatus = Column(Integer,
                     nullable=False)
    def __init__(self, pfreq):
        
        self.ffreq = pfreq
        self.fstatus = 1
    
    def __repr__(self):
        
        return f"""ID:{self.id},
                   Freq:{self.ffreq},
                   Status:{self.fstatus}"""


    
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
    freq = Column(Integer, ForeignKey(CPeriod.id))
	

    def __init__(self, pname, pdate, ptype):
        """Конструктор."""
        self.fname = pname
        self.fday = pdate.day
        self.fmonth = pdate.month
        self.fyear = pdate.year
        self.ftype = ptype

    def __repr__(self):
        
        return f"""ID:{self.id}, 
                   Name:{self.fname}, 
                   Date:{self.fday}.{self.fmonth}.{self.fyear}, 
                   Type:{self.ftype},
                   Status:{self.fstatus}"""


class CDatabase(object):
    """Класс осуществляет работу с БД."""
    def __init__(self, pdatabase_path):
        """Конструктор."""
        self.engine = create_engine('sqlite:///'+pdatabase_path)
        self.session = sessionmaker(bind=self.engine)()
        Base.metadata.bind = self.engine
        #self.session.configure(bind=self.engine)


    def create_database(self):
        """Создает или изменяет БД в соответствии с описанной в классах структурой."""
        Base.metadata.create_all()
        count = self.session.query(CEventType).count()
        if count == 0:

            event_type = CEventType("День памяти ", "#8db0bd")  #☦️
            self.session.add(event_type)
            event_type = CEventType("День рождения ", "#ecc176")  # 🎂 
            self.session.add(event_type)
            event_type = CEventType("Памятная дата - ", "#02b6ec")  #📆 
            self.session.add(event_type)
            event_type = CEventType("Напоминание: ", "#6dec04")  #🔔 
            self.session.add(event_type)
            self.session.commit()


    def delete_event(self, pid):
        """Удаляет уже существующее событие в БД."""
        event_data = self.session.query(CEvent).filter_by(id=pid)
        event_data.update({CEvent.fstatus:0}, synchronize_session = False)
        self.session.commit()


    def get_event_data(self, pid):
        """Возвращает данные события в словаре."""
        event_data = self.session.query(CEvent.fname,
                                        CEvent.fyear,
                                        CEvent.fmonth,
                                        CEvent.fday,
                                        CEvent.ftype).\
                                  filter_by(id=pid).first()
                                  #join(CEventType,CEvent.ftype).\
        return (event_data.fname,
                dt.date(event_data.fyear,
                        event_data.fmonth,
                        event_data.fday),
                event_data.ftype)


    def get_event_types_list(self):
        """Возвращает события из базы."""
        event_types_name_list = []
        event_types_id_list = []
        queried_data = self.session.query(CEventType).order_by(CEventType.fname)
        for event_type in queried_data: 
            
            event_types_name_list.append(event_type.fname)
            event_types_id_list.append(event_type.id)
        return event_types_id_list, event_types_name_list
    
    
    def get_events_list(self):
        """Возвращает события из базы."""
        event_name_list = []
        event_id_list = []
        event_data = self.session.query(CEvent.fname,
                                        CEventType.fname).join(CEventType).all()
        for event_id, event_name, event_type_name in self.session.query(CEvent.id,
                                                                        CEvent.fname,
                                                                        CEventType.fname).join(CEventType).all():
            
            
            event_name_list.append(event_type_name+event_name)
            event_id_list.append(event_id)
        return event_id_list, event_name_list


    def insert_event(self, pname, pdate, ptype):
        """Добавляет новое событие в БД."""
        event = CEvent(pname, pdate, ptype)
        self.session.add(event)
        self.session.commit()


    def update_event(self, pid, pname, pdate, ptype):
        """Изменяет уже существующее событие в БД."""
        event_data = self.session.query(CEvent).filter_by(id=pid)
        event_data.update({CEvent.fname:pname,
                           CEvent.fyear:pdate.year,
                           CEvent.fmonth:pdate.month,
                           CEvent.fday:pdate.day,
                           CEvent.ftype:ptype}, synchronize_session = False)
        self.session.commit()
