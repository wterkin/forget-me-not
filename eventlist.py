#!/usr/bin/python
# -*- coding: utf-8 -*-
#from tkinter import *
import tkinter as tk

class EventList(tk.Toplevel):
    """Класс окна списка событий."""
    def __init__(self, master, **kwargs):
        """Конструктор."""
        tk.Toplevel.__init__(self, master, **kwargs)
        # *** Фрейм кнопок
        self.list_buttons_frame = tk.Frame(self)
        self.add_button = tk.Button(#command=self.quit,
                                    master=self.list_buttons_frame,
                                    text="Добавить")
        self.add_button.pack(side=tk.LEFT)
        self.edit_button = tk.Button(#command=self.quit,
                                     master=self.list_buttons_frame,
                                     text="Редактировать")
        self.edit_button.pack(side=tk.LEFT)  # tk.RIGHT)
        self.delete_button = tk.Button(#command=self.quit,
                                       master=self.list_buttons_frame,
                                       text="Удалить")
        self.delete_button.pack(side=tk.LEFT)  # tk.RIGHT)
        self.close_button = tk.Button(command=self.quit,
                                      master=self.list_buttons_frame,
                                      text="Закрыть")
        self.close_button.pack(side=tk.RIGHT)
        self.list_buttons_frame.pack(padx=10, pady=10)
        
        # *** Фрейм списка событий
        self.events_frame = tk.Frame(self)
        self.events_box = tk.Listbox(self.events_frame)  #! , width=20, height=4)
        self.events_box.pack()
        #elf.event_type_box.curselection()
        self.events_frame.pack(padx=10, pady=10)

        # *** Показываем окно
        self.transient(master)
        self.grab_set()
        master.wait_window(self)

if __name__ == '__main__':
    master = tk.Tk()
    event_list = EventList(master)
    master.mainloop()
