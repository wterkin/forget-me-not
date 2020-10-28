#!/usr/bin/python
# -*- coding: utf-8 -*-
from tkinter import *

class EventEditor:
    def __init__(self, root):
        self.event_name_frame = Frame(root)
        self.event_name_entry = Entry(self.event_name_frame, width=20)
        self.event_name_label = Label(self.event_name_frame, width=20, text="Название события")  #  bg='black', fg='white', )

        self.event_type_frame = Frame(root)

        self.event_date_frame = Frame(root)
        self.buttons_frame = Frame(root)
        self.ok_button = Button(self.buttons_frame, text="Принять")
        self.cancel_button = Button(self.buttons_frame, text="Отмена")
        self.event_name_entry.pack()
        self.event_name_label.pack()
        self.ok_button.pack()
        self.cancel_button.pack()
        
    #b1['text'] = "Изменено"
    #b1['bg'] = '#000000'
    #b1['activebackground'] = '#555555'
    #b1['fg'] = '#ffffff'
    #b1['activeforeground'] = '#ffffff'
    #b1.config(command=change)
    #l1 = Label(text="Машинное обучение", font="Arial 32")
    #l2 = Label(text="Распознавание образов", font=("Comic Sans MS", 24, "bold"))
    #l1.config(bd=20, bg='#ffaaaa')
    #l2.config(bd=20, bg='#aaffff')
    #l1.pack()
    #l2.pack()
    #Label(text="Пункт выдачи").pack()
    #Button(text="Взять", command=take).pack()
    #lab = Label(width=10, height=1)
    #lab.pack()
if __name__ == '__main__':
    root = Tk()
    event_editor = EventEditor(root)
    root.mainloop()
