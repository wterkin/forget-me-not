#!/usr/bin/python
# -*- coding: utf-8 -*-
#from tkinter import *
import tkinter as tk

class EventList(tk.Toplevel):
    def __init__(self, root, **kwargs):
        #Tk.__init__(self)
        print("!!", **kwargs)
        tk.Toplevel().__init__(self, root, **kwargs)
        self.transient(root)
        #self.grab_set()
        root.wait_window(self)
        print("**************** 1")
        #super(EventList, self).__init__(root) # 
        #print("**************** 2")
        self.list_buttons_frame = tk.Frame(root)
        #print("**************** 3")

        self.add_button = tk.Button(#command=self.quit,
                                    master=self.list_buttons_frame,
                                    text="Добавить")
        self.add_button.pack(side=tk.LEFT)
        self.edit_button = tk.Button(#command=self.quit,
                                     master=self.list_buttons_frame,
                                     text="Редактировать")
        self.edit_button.pack(side=tk.RIGHT)
        self.delete_button = tk.Button(#command=self.quit,
                                       master=self.list_buttons_frame,
                                       text="Удалить")
        self.delete_button.pack(side=tk.RIGHT)
        self.list_buttons_frame.pack(padx=10, pady=10)
        
        self.events_frame = tk.Frame(root)
        self.events_box = tk.Listbox(self.events_frame, width=20, height=4)
        self.events_box.pack()
        #self.event_type_box.curselection()
        self.events_frame.pack(padx=10, pady=10)

        self.close_button_frame = tk.Frame(root)
        self.close_button = tk.Button(#command=self.quit,
                                      master=self.close_button_frame,
                                      text="Закрыть")
        self.close_button.pack(side=tk.RIGHT)
        self.close_button_frame.pack(padx=10, pady=10)


if __name__ == '__main__':
    root = tk.Tk()
    event_list = EventList(root)
    root.mainloop()
