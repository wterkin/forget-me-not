#!/usr/bin/python
# -*- coding: utf-8 -*-
from tkinter import *

if __name__ == '__main__':
    root = Tk()
    event_name = Entry(root, width=20)
    event_label = Label(root, width=20, text="Название события")  #  bg='black', fg='white', )
    ok_button = Button(root, text="Принять")
    cancel_button = Button(root, text="Отмена")
    event_name.pack()
    event_label.pack()
    ok_button.pack()
    cancel_button.pack()
    root.mainloop()
