#!/usr/bin/python
## -*- coding: utf-8 -*-
"""Модуль класса события."""

import c_eventtype
import c_period

class CEvent(CAncestor):
	"""Класс события."""
	
    __tablename__ = 'tbl_events'    
    fname = Column(String,
                    nullable=False)
    fday = Column(Integer,
                  nullable=False)
    fmonth = Column(Integer,
                    nullable=False)    
    fyear = Column(Integer,
                   nullable=False)    
    ftype = Column(Integer, ForeignKey(CEventType.id))
    fperiod = Column(Integer, ForeignKey(CPeriod.id))
    

    def __init__(self, pstatus, pname, pdate, ptype):
        """Конструктор."""

        super().__init__(pstatus)
        self.fname = pname
        self.fday = pdate.day
        self.fmonth = pdate.month
        self.fyear = pdate.year
        self.ftype = ptype

    def __repr__(self):
        
        return super().__repr__() +
			   f"""Name:{self.fname}, 
                   Date:{self.fday}.{self.fmonth}.{self.fyear}, 
                   Type:{self.ftype}"""


