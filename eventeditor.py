#!/usr/bin/python
# -*- coding: utf-8 -*-
import tkinter as tk
import tkcalendar as tkcal
from datetime import datetime

class EventEditor(tk.Toplevel):
    def __init__(self, pmaster, pdatabase, pid, **kwargs):
        tk.Toplevel.__init__(self, pmaster, **kwargs)
        self.master = pmaster
        self.database = pdatabase
        self.id = pid
        self.construct_window()
        if self.id is not None:
            self.load_data()
        
    def construct_window(self):
        """Создает интерфейс окна."""
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
        self.event_date_frame = tk.Frame(self)
        self.event_date_entry = tkcal.DateEntry(self.event_date_frame,
                                    width=12,
                                    #background='darkblue',
                                    #foreground='white',
                                    borderwidth=2)        
        self.event_date_entry.pack()
        self.event_date_frame.pack(padx=10,
                                   pady=10)

        # *** Кнопки 
        self.buttons_frame = tk.Frame(self)
        self.ok_button = tk.Button(command=self.save_data,
                                   master=self.buttons_frame,
                                   text="Принять")
        self.ok_button.pack(side=tk.LEFT)
        self.cancel_button = tk.Button(command=self.quit,
                                       master=self.buttons_frame,
                                       text="Отмена")
        self.cancel_button.pack(side=tk.RIGHT)
        self.buttons_frame.pack(padx=10,
                                pady=10)
        
        self.transient(self.master)
        self.grab_set()
        self.master.wait_window(self)
        
        
    def load_data(self):
        """Процедура загрузки данных в контролы."""
        pass
    
    def save_data(self):
        """Сохраняет введённые данные."""
        date_str = self.event_date_entry.get()
        date_date = datetime.strptime(date_str, "%d.%m.%Y")
        selected_items = self.event_type_box.curselection()
        #date_dt3 = datetime.strptime(date_str3, '%m-%d-%Y')
        #print("^^^^^ ", self.event_date_entry.get())
        self.database.insert_event(self.event_name_entry.get().strip(),
                                   date_date,
                                   selected_items[0])
        self.destroy()
    
if __name__ == '__main__':
    root = tk.Tk()  
    event_editor = EventEditor(root)
    root.mainloop()
