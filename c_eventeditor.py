#!/usr/bin/python
# -*- coding: utf-8 -*-
import tkinter as tk
import tkcalendar as tkcal
from datetime import datetime

class EventEditor(tk.Toplevel):
    def __init__(self, pmaster, pdatabase, pid, **kwargs):
        # *** Конструктор
        tk.Toplevel.__init__(self, pmaster, **kwargs)
        self.master = pmaster
        self.database = pdatabase
        self.id = pid
        self.event_period_var = BooleanVar()
        self.event_period_var.set(0)
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

        # *** Тип и период события
        self.event_type_frame = tk.Frame(self)
        self.event_type_box = tk.Listbox(self.event_type_frame,
                                         height=4,
                                         width=20)
        self.event_type_box.pack(side=tk.LEFT)
        
        self.period_monthly_rb = tk.Radiobutton(indicatoron=1,
                                          master=self.event_type_frame,
                                          text="Ежемесячно",
                                          value=0,
                                          variable=self.event_period_var
                                          )
        self.period_monthly_rb.pack(side=tk.RIGHT)  # anchor=tk.W)
        self.period_yearly_rb = tk.Radiobutton(indicatoron=1,
                                          master=self.event_type_frame,
                                          text="Ежегодно  ",
                                          value=1,
                                          variable=self.event_period_var
                                          )
        self.period_yearly_rb.pack(side=tk.RIGHT)  # anchor=W)
        
        self.event_type_frame.pack(padx=10,
                                   pady=10)
      
        # *** Дата события
        self.event_date_frame = tk.Frame(self)
        self.event_date_entry = tkcal.DateEntry(self.event_date_frame,
                                    width=12,
                                    locale="ru_RU",
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
        event_name, event_date, event_type, event_period = self.database.get_event_data(self.id)
        # print("EVED.LD.EVID ", self.id)
        # print("EVED.LD.EVN ", event_name)
        # print("EVED.LD.EVN ", event_date)
        # print("EVED.LD.EVN ", self.event_type)
        self.event_name_entry.insert(tk.END, event_name)
        self.event_date_entry.set_date(event_date)
        self.event_type_box.select_set(self.event_types_id_list.index(event_type))
        self.event_period_var.set(event_period)
    
    def load_event_types_list(self):
        """Загружает список типов событий в listbox."""
        self.event_types_id_list, event_types_name_list = self.database.get_event_types_list()
        for event_name in event_types_name_list:
            self.event_type_box.insert(tk.END, event_name)
    
    
    def save_data(self):
        """Сохраняет введённые данные."""
        # print("*** ", self.event_date_entry.get())
        # print("*** ", datetime.strptime(self.event_date_entry.get(), "%d.%m.%Y"))
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
                                       event_type,
                                       self.event_period_var)
        else:

            self.database.update_event(self.id, 
                                       self.event_name_entry.get().strip(),
                                       event_date,
                                       event_type,
                                       self.event_period_var)
                                       
        self.destroy()
    
    
if __name__ == '__main__':
    root = tk.Tk()  
    event_editor = EventEditor(root)
    root.mainloop()
