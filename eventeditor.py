#!/usr/bin/python
# -*- coding: utf-8 -*-
import tkinter as tk

class EventEditor(tk.Toplevel):
    def __init__(self, pmaster, **kwargs):
        tk.Toplevel.__init__(self, pmaster, **kwargs)
        self.master = pmaster
        
        # *** Наименование события
        self.event_name_frame = tk.Frame(self)
        self.event_name_entry = tk.Entry(self.event_name_frame,
                                         width=20)
        self.event_name_entry.pack(side=tk.RIGHT)
        self.event_name_label = tk.Label(self.event_name_frame,
                                         text="Название события",
                                         width=20) #  bg='black', fg='white', )
        self.event_name_label.pack(side=tk.LEFT)
        self.event_name_frame.pack(padx=10,
                                   pady=10)

        # *** Тип события 
        self.event_type_frame = tk.Frame(self)
        self.event_type_box = tk.Listbox(self.event_type_frame,
                                         height=4,
                                         width=20)
        self.event_type_box.insert(0, "День памяти")
        self.event_type_box.insert(1, "День рождения")
        self.event_type_box.insert(2, "Памятная дата")
        self.event_type_box.insert(3, "Напоминание")
        self.event_type_box.pack()
        self.event_type_frame.pack(padx=10,
                                   pady=10)
      
        # *** Дата события
        
        # *** Кнопки 
        self.buttons_frame = tk.Frame(self)
        self.ok_button = tk.Button(command=self.quit,
                                   master=self.buttons_frame,
                                   text="Принять")
        self.ok_button.pack(side=tk.LEFT)
        self.cancel_button = tk.Button(command=self.quit,
                                       master=self.buttons_frame,
                                       text="Отмена")
        self.cancel_button.pack(side=tk.RIGHT)
        self.buttons_frame.pack(padx=10,
                                pady=10)
        
if __name__ == '__main__':
    root = tk.Tk()
    event_editor = EventEditor(root)
    root.mainloop()
