#!/usr/bin/python
## -*- coding: utf-8 -*-

from sqlalchemy import create_engine # Table Column   Integer, String, MetaData, ForeignKey,
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import datetime as dt

import c_ancestor
import c_config
import c_eventtype
#import c_period
import c_event      

class CDatabase(object):
    """Класс осуществляет работу с БД."""
    def __init__(self, pconfig):
        """Конструктор."""
        self.config = pconfig
        self.engine = create_engine('sqlite:///'+self.config.restore_value(c_config.DATABASE_FILE_KEY))
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session = Session()
        c_ancestor.Base.metadata.bind = self.engine


    def create_database(self):
        """Создает или изменяет БД в соответствии с описанной в классах структурой."""
        c_ancestor.Base.metadata.create_all()
        count = self.session.query(c_eventtype.CEventType).count()
        if count == 0:

            event_type = c_eventtype.CEventType(1, "День памяти ", "#8db0bd", "☦️")
            self.session.add(event_type)
            event_type = c_eventtype.CEventType(1, "День рождения ", "#ecc176", "🎂")
            self.session.add(event_type)
            event_type = c_eventtype.CEventType(1, "Памятная дата - ", "#02b6ec", "📆")
            self.session.add(event_type)
            event_type = c_eventtype.CEventType(1, "Напоминание: ", "#6dec04", "🔔")
            self.session.add(event_type)
            self.session.commit()


    def delete_event(self, pid):
        """Удаляет уже существующее событие в БД."""
        event_data = self.session.query(c_event.CEvent).filter_by(id=pid)
        event_data.update({c_event.CEvent.fstatus:0}, synchronize_session = False)
        self.session.commit()


    def actual_monthly_events(self):
        """Возвращает список событий, актуальных в периоде от текущей даты до текущей + период видимости."""
        # *** Дата по = текущая+период
        #date_to = dt.now() + dt.timedelta(days=int(self.config.restore_value(c_config.MONITORING_PERIOD_KEY)))
        
        # *** Если дата по в следующем месяце...
        # ***   разделяем период на два отрезка - от текущей даты до конца м-ца и от нач. м-ца до даты по 
        # ***   делаем две выборки или union
        # *** Иначе 
        # ***   делаем одну выборку

    def get_event_data(self, pid):
        """Возвращает данные события в словаре."""
        event_data = self.session.query(c_event.CEvent.fname,
                                        c_event.CEvent.fyear,
                                        c_event.CEvent.fmonth,
                                        c_event.CEvent.fday,
                                        c_event.CEvent.ftype).\
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
        queried_data = self.session.query(c_eventtype.CEventType).order_by(c_eventtype.CEventType.fname)
        # ToDo: вот тут не доделал!
        for event_type in queried_data:
            
            event_types_name_list.append(event_type.fname)
            event_types_id_list.append(event_type.id)
        return event_types_id_list, event_types_name_list
    
    
    def get_events_list(self):
        """Возвращает события из базы."""
        event_name_list = []
        event_id_list = []
        # event_data = self.session.query(c_event.CEvent.fname,
                                        # c_eventtype.CEventType.fname).join(c_eventtype.CEventType).all()
        for event_id, event_name, event_type_name in self.session.query(c_event.CEvent.id,
                                                                        c_event.CEvent.fname,
                                                                        c_eventtype.CEventType.fname).join(c_eventtype.CEventType).all():
            
            
            event_name_list.append(event_type_name+event_name)
            event_id_list.append(event_id)
        return event_id_list, event_name_list


    def insert_event(self, pname, pdate, ptype):
        """Добавляет новое событие в БД."""
        event = c_event.CEvent(1, pname, pdate, ptype)
        self.session.add(event)
        self.session.commit()


    def update_event(self, pid, pname, pdate, ptype):
        """Изменяет уже существующее событие в БД."""
        event_data = self.session.query(c_event.CEvent).filter_by(id=pid)
        event_data.update({c_event.CEvent.fname:pname,
                           c_event.CEvent.fyear:pdate.year,
                           c_event.CEvent.fmonth:pdate.month,
                           c_event.CEvent.fday:pdate.day,
                           c_event.CEvent.ftype:ptype}, synchronize_session = False)
        self.session.commit()
