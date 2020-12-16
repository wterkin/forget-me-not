#!/usr/bin/python
## -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_

import datetime as dtime
from datetime import datetime as dt


import c_ancestor
import c_config
import c_eventtype
#import c_period
import c_event  
import c_tools as tls    

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


    def actual_monthly_events(self):
        """Возвращает список событий, актуальных в периоде от текущей даты до текущей + период видимости."""
        # *** Дата по = текущая+период
        date_from = dt.now().date()
        print("*** DB.AME.df ", date_from)
        # *** Если дата по в следующем месяце разделяем период на два отрезка - 
        #     от текущей даты до конца м-ца и от нач. м-ца до даты по 
        date_to =  date_from + dtime.timedelta(days=int(self.config.restore_value(c_config.MONITORING_PERIOD_KEY)))
        print("*** DB.AME.dt ", date_to)
        if date_to.month != date_from.month:
            
            last_day = tls.get_months_last_date(date_from)
            this_month_date_to = dtime.datetime(date_from.year, date_from.month, last_day)
            print("*** DB.AME.tmdt ", this_month_date_to)
            
            next_month_date_from = this_month_date_to + dtime.timedelta(days=1)
            print("*** DB.AME.nmdf ", next_month_date_from)
            
            # ***   делаем две выборки или union
            queried_data1 = self.session.query(c_event.CEvent)
            queried_data1 = queried_data1.filter(c_event.CEvent.fyear>=date_from.year, 
                                                 and_(c_event.CEvent.fmonth>=date_from.month, 
                                                 and_(c_event.CEvent.fday<=date_from.day,
                                                 and_(c_event.CEvent.fyear<=this_month_date_to.year,
                                                 and_(c_event.CEvent.fmonth<=this_month_date_to.month,
                                                 and_(c_event.CEvent.fday<=this_month_date_to.day))))))
            queried_data2 = self.session.query(c_event.CEvent)
            queried_data2 = queried_data2.filter(c_event.CEvent.fyear>=next_month_date_from.year, 
                                                 and_(c_event.CEvent.fmonth>=next_month_date_from.month, 
                                                 and_(c_event.CEvent.fday>=next_month_date_from.day,
                                                 and_(c_event.CEvent.fyear<=date_to.year,
                                                 and_(c_event.CEvent.fmonth<=date_to.month,
                                                 and_(c_event.CEvent.fday<=date_to.day))))))
            query = queried_data1.union(queried_data2)
            query = query.all()
            return query
            # .order_by(c_eventtype.CEventType.fname)
            
            
        else:
            
            pass
        
        # *** Иначе 
        # ***   делаем одну выборку


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


    def get_event_data(self, pid): # +
        """Возвращает данные события."""
        event_data = self.session.query(c_event.CEvent.fname,
                                        c_event.CEvent.fyear,
                                        c_event.CEvent.fmonth,
                                        c_event.CEvent.fday,
                                        c_event.CEvent.ftype).\
                                  filter_by(id=pid).first()
        return (event_data.fname,
                dt.date(event_data.fyear,
                        event_data.fmonth,
                        event_data.fday),
                event_data.ftype)


    def get_event_types_list(self): # +
        """Возвращает события из базы."""
        event_types_name_list = []
        event_types_id_list = []
        queried_data = self.session.query(c_eventtype.CEventType).order_by(c_eventtype.CEventType.fname)
        for event_type in queried_data:
            
            event_types_name_list.append(event_type.fname)
            event_types_id_list.append(event_type.id)
        return event_types_id_list, event_types_name_list
    
    
    def get_events_list(self): # +
        """Возвращает события из базы."""
        event_name_list = []
        event_id_list = []
        query = self.session.query(c_event.CEvent.id, c_event.CEvent.fname, c_eventtype.CEventType.fname)
        query = query.join(c_eventtype.CEventType)
        query = query.all()
        for event_id, event_name, event_type_name in query:
            
            event_name_list.append(event_type_name+event_name)
            event_id_list.append(event_id)
        return event_id_list, event_name_list


    def insert_event(self, pname, pdate, ptype): # +
        """Добавляет новое событие в БД."""
        event = c_event.CEvent(1, pname, pdate, ptype)
        self.session.add(event)
        self.session.commit()


    def update_event(self, pid, pname, pdate, ptype): # +
        """Изменяет уже существующее событие в БД."""
        event_data = self.session.query(c_event.CEvent).filter_by(id=pid)
        event_data.update({c_event.CEvent.fname:pname,
                           c_event.CEvent.fyear:pdate.year,
                           c_event.CEvent.fmonth:pdate.month,
                           c_event.CEvent.fday:pdate.day,
                           c_event.CEvent.ftype:ptype}, synchronize_session = False)
        self.session.commit()
