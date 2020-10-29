#!/usr/bin/python
## -*- coding: utf-8 -*-

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

metadata = MetaData()

class EventTypes(object):
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
