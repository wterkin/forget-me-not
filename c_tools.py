#!/usr/bin/python
## -*- coding: utf-8 -*-
"""Модуль всякой полезной всячины."""

import c_constants as cnst
# from datetime import datetime as dt
import calendar

def center_window(pwindow, pwindow_width, pwindow_height):
    """Центрует заданное окно."""
    screen_width = pwindow.winfo_screenwidth()
    screen_height = pwindow.winfo_screenheight()
    window_left = (screen_width - pwindow_width) // 2
    window_top = (screen_height - pwindow_height) // 2
    return window_left, window_top


# def set_window_size(window, width, height):
    # """Устанавливает размеры окна."""
    # print("*** SWS ",  width, height)
    # window.geometry('%dx%d+%d+%d' % (width, height, 0, 0))

def get_months_last_date(pdate):
    """Возвращает первый день месяца"""
    return calendar.monthrange(pdate.year, pdate.month)[1]
    # if pdate.month == 12: # December
        # last_day_selected_month = dtime.datetime(pdate.year, pdate.month, 31)
    # else:
        # last_day_selected_month = dtime.datetime(pdate.year, pdate.month + 1, 1) - timedelta(days=1)
    # return last_day_selected_month    