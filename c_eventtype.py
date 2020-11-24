#!/usr/bin/python
## -*- coding: utf-8 -*-
"""Модуль класса типа события Alchemy"""

import c_ancestor

class CEventType(CAncestor):
	"""Класс типов событий."""

    __tablename__ = 'tbl_types'
    fname = Column(String,
                    nullable=False,
                    unique=True)
    fcolor = Column(String,
                    nullable=False)
    femodji = Column(String,
                     nullable=True)

    def __init__(self, pstatus, pname, pcolor, pemodji):
        """Конструктор"""
        super().__init__(pstatus)
        self.fname = pname
        self.fcolor = pcolor
		self.femodji = pemodji
		
    def __repr__(self):
	    return super().__repr__() +
			   f"""Name:{self.fname},
                   Color:{self.fcolor},
                   Emodji:{self.femodji}"""

