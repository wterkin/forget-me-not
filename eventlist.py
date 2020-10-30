#!/usr/bin/python
# -*- coding: utf-8 -*-
from tkinter import *

class EventList(Toplevel):
    def __init__(self, root):
        Frame.__init__(self, root) # background = "white"
        self.list_buttons_frame = Frame(root)
        self.add_button = Button(#command=self.quit,
                                 master=self.list_buttons_frame,
                                 text="Добавить")
        self.add_button.pack(side=LEFT)
        self.edit_button = Button(#command=self.quit,
                                  master=self.list_buttons_frame,
                                  text="Редактировать")
        self.edit_button.pack(side=RIGHT)
        self.delete_button = Button(#command=self.quit,
                                    master=self.list_buttons_frame,
                                    text="Удалить")
        self.delete_button.pack(side=RIGHT)
        self.list_buttons_frame.pack(padx=10, pady=10)
        
        self.events_frame = Frame(root)
        self.events_box = Listbox(self.events_frame, width=20, height=4)
        self.events_box.pack()
        #self.event_type_box.curselection()
        self.events_frame.pack(padx=10, pady=10)

        self.close_button_frame = Frame(root)
        self.close_button = Button(#command=self.quit,
                                    master=self.close_button_frame,
                                    text="Закрыть")
        self.close_button.pack(side=RIGHT)
        self.close_button_frame.pack(padx=10, pady=10)


if __name__ == '__main__':
    root = Tk()
    event_list = EventList(root)
    root.mainloop()
