#!/usr/bin/python
## -*- coding: utf-8 -*-
"""Модуль всякой полезной всячины."""

import c_constants as cnst


def center_window(window):
    """Центрует заданное окно."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_left = (screen_width - cnst.MAIN_WINDOW_WIDTH) // 2
    window_top = (screen_height - cnst.MAIN_WINDOW_HEIGHT) // 2
    return window_left, window_top


# def set_window_size(window, width, height):
    # """Устанавливает размеры окна."""
    # print("*** SWS ",  width, height)
    # window.geometry('%dx%d+%d+%d' % (width, height, 0, 0))

