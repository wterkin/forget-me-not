#!/usr/bin/python
# -*- coding: utf-8 -*-
from tkinter import *

class EventEditor:
    def __init__(self, root):
        self.event_name = Entry(root, width=20)
        self.event_label = Label(root, width=20, text="Название события")  #  bg='black', fg='white', )
        self.ok_button = Button(root, text="Принять")
        self.cancel_button = Button(root, text="Отмена")
        self.event_name.pack()
        self.event_label.pack()
        self.ok_button.pack()
        self.cancel_button.pack()
        
    #b1['text'] = "Изменено"
    #b1['bg'] = '#000000'
    #b1['activebackground'] = '#555555'
    #b1['fg'] = '#ffffff'
    #b1['activeforeground'] = '#ffffff'
    #b1.config(command=change)
    
if __name__ == '__main__':
    root = Tk()
    event_editor = EventEditor(root)
    root.mainloop()
