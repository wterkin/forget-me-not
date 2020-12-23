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
import c_constants as const

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
          


    def convert_monthly_tuple(pevent_super_tuple, pnew_date):
        """Конвертирует кортеж в список, подставляя значения года и месяца из даты."""
        event_super_list = []
        for event_tuple in pevent_super_tuple:

            event_list = list(event_tuple)
            event_list[3] = pnew_date.year
            event_list[2] = pnew_date.month
            event_super_list.append(event_list)
        return event_super_list    


    def convert_yearly_tuple(pevent_super_tuple, pnew_date):
        """Конвертирует кортеж в список, подставляя значения года и месяца из даты."""
        event_super_list = []
        for event_tuple in pevent_super_tuple:

            event_list = list(event_tuple)
            event_list[3] = pnew_date.year
            event_super_list.append(event_list)
        return event_super_list    


    def create_database(self):
        """Создает или изменяет БД в соответствии с описанной в классах структурой."""
        c_ancestor.Base.metadata.create_all()
        count = self.session.query(c_eventtype.CEventType).count()
        if count == 0:

            fill_event_types_table()
        count = self.session.query(c_period.CPeriod).count()
        if count == 0:

            fill_periods_table()


    def delete_event(self, pid):
        """Удаляет уже существующее событие в БД."""
        event_data = self.session.query(c_event.CEvent).filter_by(id=pid)
        event_data.update({c_event.CEvent.fstatus:0}, synchronize_session = False)
        self.session.commit()


    def fill_event_types_table():
        """Заполняет пустую таблицу справочника типов событий значениями."""
        event_type = c_eventtype.CEventType(1, "День памяти ", "#8db0bd", "☦️")
        self.session.add(event_type)
        event_type = c_eventtype.CEventType(1, "День рождения ", "#ecc176", "🎂")
        self.session.add(event_type)
        event_type = c_eventtype.CEventType(1, "Памятная дата - ", "#02b6ec", "📆")
        self.session.add(event_type)
        event_type = c_eventtype.CEventType(1, "Напоминание: ", "#6dec04", "🔔")
        self.session.add(event_type)
        self.session.commit()


    def fill_periods_table():
        """Заполняет пустую таблицу справочника периодов значениями."""
        period_type = c_period.CPeriod(1, "Ежемесячное событие")
        self.session.add(period_type)
        period_type = c_period.CPeriod(1, "Ежегодное событие")
        self.session.add(period_type)
        period_type = c_period.CPeriod(1, "Единовременное событие")
        self.session.add(period_type)
        self.session.commit()


    def get_actual_monthly_events(self):
        """Возвращает список ежемесячных событий, актуальных в периоде от текущей даты до текущей + период видимости."""
        # *** Дата по = текущая+период
        date_from = dt.now().date()
        # *** Если дата по в следующем месяце разделяем период на два отрезка - 
        #     от текущей даты до конца м-ца и от нач. м-ца до даты по 
        date_to =  date_from + dtime.timedelta(days=int(self.config.restore_value(c_config.MONITORING_PERIOD_KEY)))
        if date_to.month != date_from.month:
            
            last_day = tls.get_months_last_date(date_from)
            this_month_date_to = dtime.datetime(date_from.year, date_from.month, last_day)
            next_month_date_from = this_month_date_to + dtime.timedelta(days=1)
            # *** делаем две выборки
            queried_data1 = self.session.query(c_event.CEvent.fname,
                                               c_event.CEvent.fday,
                                               c_event.CEvent.fmonth,
                                               c_event.CEvent.fyear,
                                               c_event.CEvent.ftype,
                                               c_event.CEvent.fperiod,
                                               c_eventtype.CEventType.fname,
                                               c_eventtype.CEventType.fcolor,
                                               c_eventtype.CEventType.femodji)
            queried_data1 = queried_data1.join(c_eventtype.CEventType)
            queried_data1 = queried_data1.filter(c_event.CEvent.fperiod==const.EVENT_MONTH_PERIOD, 
                                                 and_(c_event.CEvent.fday>=date_from.day,
                                                 and_(c_event.CEvent.fday<=this_month_date_to.day)))
            queried_data1 = queried_data1.order_by(c_event.CEvent.fday)
            queried_data1 = convert_monthly_tuple(queried_data1.all(), this_month_date_to)
            
            queried_data2 = self.session.query(c_event.CEvent.fname,
                                               c_event.CEvent.fday,
                                               c_event.CEvent.fmonth,
                                               c_event.CEvent.fyear,
                                               c_event.CEvent.ftype,
                                               c_event.CEvent.fperiod,
                                               c_eventtype.CEventType.fname,
                                               c_eventtype.CEventType.fcolor,
                                               c_eventtype.CEventType.femodji)
            queried_data2 = queried_data2.join(c_eventtype.CEventType)
            queried_data2 = queried_data2.filter(c_event.CEvent.fperiod==const.EVENT_MONTH_PERIOD, 
                                                 and_(c_event.CEvent.fday>=next_month_date_from.day,
                                                 and_(c_event.CEvent.fday<=date_to.day)))
            queried_data2 = queried_data2.order_by(c_event.CEvent.fday)
            queried_data2 = convert_monthly_tuple(queried_data2.all(), next_month_date_from)
            queried_data1.extend(queried_data2)
            return queried_data1
        else:

            # *** Иначе делаем одну выборку
            queried_data = self.session.query(c_event.CEvent.fname,
                                              c_event.CEvent.fday,
                                              c_event.CEvent.fmonth,
                                              c_event.CEvent.fyear,
                                              c_event.CEvent.ftype,
                                              c_event.CEvent.fperiod,
                                              c_eventtype.CEventType.fname,
                                              c_eventtype.CEventType.fcolor,
                                              c_eventtype.CEventType.femodji)
            queried_data = queried_data.join(c_eventtype.CEventType)
            queried_data = queried_data.filter(c_event.CEvent.fperiod==const.EVENT_MONTH_PERIOD, 
                                               and_(c_event.CEvent.fday>=date_from.day,
                                               and_(c_event.CEvent.fday<=date_to.day)))
            queried_data = queried_data.order_by(c_event.CEvent.fmonth, c_event.CEvent.fday)
            queried_data = convert_monthly_tuple(queried_data.all(), date_from)
            return queried_data
        

    def get_actual_yearly_events(self):
        """Возвращает список ежегодных событий, актуальных в периоде от текущей даты до текущей + период видимости."""
        # *** Дата с..
        date_from = dt.now().date()
        # *** Дата по..
        date_to =  date_from + dtime.timedelta(days=int(self.config.restore_value(c_config.MONITORING_PERIOD_KEY)))
        # *** Если дата по в следующем году разделяем период на два отрезка - 
        #     от текущей даты до конца года и от нач. года до даты по 
        if date_to.year != date_from.year:
            
            last_day = tls.get_years_last_date(date_from)
            this_year_date_to = dtime.datetime(date_from.year, date_from.month, last_day)
            
            next_year_date_from = this_year_date_to + dtime.timedelta(days=1)
            # *** делаем две выборки
            queried_data1 = self.session.query(c_event.CEvent.fname,
                                               c_event.CEvent.fday,
                                               c_event.CEvent.fmonth,
                                               c_event.CEvent.fyear,
                                               c_event.CEvent.ftype,
                                               c_event.CEvent.fperiod,
                                               c_eventtype.CEventType.fname,
                                               c_eventtype.CEventType.fcolor,
                                               c_eventtype.CEventType.femodji)
            queried_data1 = queried_data1.join(c_eventtype.CEventType)
            queried_data1 = queried_data1.filter(c_event.CEvent.fperiod==const.EVENT_YEAR_PERIOD, 
                                                 and_(c_event.CEvent.fday>=date_from.day,
                                                 and_(c_event.CEvent.fmonth>=date_from.month,
                                                 and_(c_event.CEvent.fday<=this_year_date_to.day,
                                                 and_(c_event.CEvent.fmonth<=this_year_date_to.month)))))
            queried_data1 = queried_data1.order_by(c_event.CEvent.fmonth, c_event.CEvent.fday)
            queried_data1 = queried_data1.all()
            convert_yearly_tuple(queried_data1, this_year_date_to)
            # Вторая выборка
            queried_data2 = self.session.query(c_event.CEvent.fname,
                                               c_event.CEvent.fday,
                                               c_event.CEvent.fmonth,
                                               c_event.CEvent.fyear,
                                               c_event.CEvent.ftype,
                                               c_event.CEvent.fperiod,
                                               c_eventtype.CEventType.fname,
                                               c_eventtype.CEventType.fcolor,
                                               c_eventtype.CEventType.femodji)
            queried_data2 = queried_data2.join(c_eventtype.CEventType)
            queried_data2 = queried_data2.filter(c_event.CEvent.fperiod==const.EVENT_YEAR_PERIOD, 
                                                 and_(c_event.CEvent.fday>=next_year_date_from.day,
                                                 and_(c_event.CEvent.fmonth>=next_year_date_from.month,
                                                 and_(c_event.CEvent.fday<=date_to.day,
                                                 and_(c_event.CEvent.fmonth<=date_to.month)))))
            queried_data2 = queried_data2.order_by(c_event.CEvent.fmonth, c_event.CEvent.fday)
            queried_data2 = queried_data2.all()
            convert_yearly_tuple(queried_data2, next_year_date_from)

            queried_data1.extend(queried_data2)
            return queried_data1
        else:
            
            # *** Иначе делаем одну выборку
            queried_data = self.session.query(c_event.CEvent.fname,
                                              c_event.CEvent.fday,
                                              c_event.CEvent.fmonth,
                                              c_event.CEvent.fyear,
                                              c_event.CEvent.ftype,
                                              c_event.CEvent.fperiod,
                                              c_eventtype.CEventType.fname,
                                              c_eventtype.CEventType.fcolor,
                                              c_eventtype.CEventType.femodji)
            queried_data = queried_data.join(c_eventtype.CEventType)
            queried_data = queried_data.filter(c_event.CEvent.fperiod==const.EVENT_YEAR_PERIOD, 
                                               and_(c_event.CEvent.fday>=date_from.day,
                                               and_(c_event.CEvent.fmonth>=date_from.fmonth,
                                               and_(c_event.CEvent.fday<=date_to.day,
                                               and_(c_event.CEvent.fmonth<=date_to.fmonth)))))
            queried_data = queried_data.order_by(c_event.CEvent.fmonth, c_event.CEvent.fday)
            queried_data = queried_data.all()
            convert_monthly_tuple(queried_data, date_from)
            return queried_data
            

    def get_event_data(self, pid): # +
        """Возвращает данные события."""
        event_data = self.session.query(c_event.CEvent.fname,
                                        c_event.CEvent.fyear,
                                        c_event.CEvent.fmonth,
                                        c_event.CEvent.fday,
                                        c_event.CEvent.ftype,
                                        c_event.CEvent.fperiod).\
                                  filter_by(id=pid).first()
        return (event_data.fname,
                dtime.datetime(event_data.fyear,
                               event_data.fmonth,
                               event_data.fday),
                event_data.ftype,
                event_data.fperiod)


    def get_event_types_list(self): # +
        """Возвращает список ID и наименований типов событий."""
        event_types_name_list = []
        event_types_id_list = []
        queried_data = self.session.query(c_eventtype.CEventType).order_by(c_eventtype.CEventType.fname)
        for event_type in queried_data:
            
            event_types_name_list.append(event_type.fname)
            event_types_id_list.append(event_type.id)
        return event_types_id_list, event_types_name_list


    def get_periods_list(self): # +
        """Возвращает список ID и наименований периодов."""
        periods_name_list = []
        periods_id_list = []
        queried_data = self.session.query(c_period.CPeriod).order_by(c_period.CPeriod.id)
        for period in queried_data:
            
            periods_name_list.append(period.fname)
            periods_id_list.append(period.id)
        return periods_id_list, periods_name_list
    
    
    
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


    def insert_event(self, pname, pdate, ptype, pperiod): # +
        """Добавляет новое событие в БД."""
        event = c_event.CEvent(1, pname, pdate, ptype, pperiod)
        self.session.add(event)
        self.session.commit()


    def update_event(self, pid, pname, pdate, ptype, pperiod): # +
        """Изменяет уже существующее событие в БД."""
        event_data = self.session.query(c_event.CEvent).filter_by(id=pid)
        event_data.update({c_event.CEvent.fname:pname,
                           c_event.CEvent.fyear:pdate.year,
                           c_event.CEvent.fmonth:pdate.month,
                           c_event.CEvent.fday:pdate.day,
                           c_event.CEvent.ftype:ptype,
                           c_event.CEvent.fperiod:pperiod}, synchronize_session = False)
        self.session.commit()
