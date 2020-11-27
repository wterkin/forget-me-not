#!/usr/bin/python
## -*- coding: utf-8 -*-
"""Модуль всякой полезной всячины."""

def get_window_size(window):
    """Возвращает размеры окна."""
    size = window.geometry()
    #1x1+640+300
    size_list = size.split('+')
    print("*** GWS", size_list)
    return int(size_list[1]), int(size_list[2])


def center_window(window):
    """Центрует заданное окно."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width, window_height = get_window_size(window)
    print("*** CW ", screen_width, screen_height)
    print("*** CW ", window_width, window_height)
    
    window_left = (screen_width - window_width) // 2
    window_top = (screen_height - window_height) // 2
    window.geometry('%dx%d+%d+%d' % (window_width, window_height, window_left, window_top))


# def set_window_size(window, width, height):
    # """Устанавливает размеры окна."""
    # print("*** SWS ",  width, height)
    # window.geometry('%dx%d+%d+%d' % (width, height, 0, 0))

