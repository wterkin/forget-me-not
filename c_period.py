#!/usr/bin/python
## -*- coding: utf-8 -*-
"""Модуль класса периода события Alchemy"""

from sqlalchemy import Table, Column, Integer

import c_ancestor

class CPeriod(c_ancestor.CAncestor):
	
    __tablename__ = 'tbl_periods'
    fperiod = Column(Integer,
                     nullable=False)

    def __init__(self, pstatus, pperiod):
        """Конструктор."""
        super().__init__(pstatus)
        self.fperiod = pperiod
    
    def __repr__(self):
        return f"""{ancestor_repr}
				   Period:{self.fperiod}"""
