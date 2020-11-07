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
        else:

            # *** Загрузим список типов событий
            self.load_event_types_list()
            
        self.transient(self.master)
        self.grab_set()
        self.master.wait_window(self)
        
        
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
        self.cancel_button = tk.Button(command=self.destroy,
                                       master=self.buttons_frame,
                                       text="Отмена")
        self.cancel_button.pack(side=tk.RIGHT)
        self.buttons_frame.pack(padx=10,
                                pady=10)
        
    
    def load_data(self):
        """Процедура загрузки данных в контролы."""
        self.load_event_types_list()
        event_name, event_date, self.event_type = self.database.get_event_data(self.id)
        self.event_name_entry.insert(tk.END, event_name)
        self.event_date_entry.set_date(event_date)
        self.event_type_box.select_set(self.event_types_id_list.index(self.event_type))
    
    
    def load_event_types_list(self):
        """Загружает список типов событий в listbox."""
        self.event_types_id_list, event_types_name_list = self.database.get_event_types_list()
        for event_name in event_types_name_list:
            self.event_type_box.insert(tk.END, event_name)
    
    
    def save_data(self):
        """Сохраняет введённые данные."""
        event_date = datetime.strptime(self.event_date_entry.get(), "%d.%m.%Y")
        selected_items = self.event_type_box.curselection()
        # *** Если внезапно в листбоксе нет выбранного элемента - используем сохраненный ID
        if len(selected_items) == 0:
        
            event_type = self.event_type
        else:
            
            event_type = self.event_types_id_list[selected_items[0]]
        
        if self.id is None:

            self.database.insert_event(self.event_name_entry.get().strip(),
                                       event_date,
                                       event_type)
        else:

            self.database.update_event(self.id, 
                                       self.event_name_entry.get().strip(),
                                       event_date,
                                       event_type)
                                       
        self.destroy()
    
    
if __name__ == '__main__':
    root = tk.Tk()  
    event_editor = EventEditor(root)
    root.mainloop()
