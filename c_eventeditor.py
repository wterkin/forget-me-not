#!/usr/bin/python
# -*- coding: utf-8 -*-
import tkinter as tk
import tkcalendar as tkcal
from datetime import datetime

import c_constants as cnst
import c_tools as tls

class EventEditor(tk.Toplevel):
    def __init__(self, pmaster, pdatabase, pid, **kwargs):
        # *** Конструктор
        tk.Toplevel.__init__(self, pmaster, **kwargs)
        self.master = pmaster
        self.database = pdatabase
        self.id = pid
        self.event_period_var = tk.IntVar()
        self.event_period_var.set(0)
        #self.event_type = 0
        self.construct_window()
        # *** Загрузим список типов событий
        self.load_event_types_list()
        # *** Загрузим список периодов
        self.load_periods_list()
        if self.id is not None:

            self.load_data()
            
        self.focus_set()
        self.transient(self.master)
        self.grab_set()
        self.master.wait_window(self)
        
        
    def construct_window(self):
        """Создает интерфейс окна."""
        # *** Наименование события
        window_left, window_top = tls.center_window(self, cnst.EVENT_EDITOR_WINDOW_WIDTH, cnst.EVENT_EDITOR_WINDOW_HEIGHT)
        window_geometry = f"{cnst.EVENT_EDITOR_WINDOW_WIDTH}x{cnst.EVENT_EDITOR_WINDOW_HEIGHT}+{window_left}+{window_top}"
        self.geometry(window_geometry)
        self.update_idletasks()

        self.event_name_frame = tk.Frame(self)
        self.event_name_entry = tk.Entry(self.event_name_frame,
                                         width=20)
        self.event_name_entry.pack(side=tk.RIGHT)
        self.event_name_entry.focus()
        self.event_name_label = tk.Label(self.event_name_frame,
                                         text="Название события",
                                         width=20) #  bg='black', fg='white', )
        self.event_name_label.pack(side=tk.LEFT)
        self.event_name_frame.pack(padx=10,
                                   pady=10)

        # *** Тип и период события
        self.options_frame = tk.Frame(self)
        self.event_type_box = tk.Listbox(self.options_frame,
                                         height=6,
                                         width=30)
        
        self.event_period_box = tk.Listbox(self.options_frame,
                                           height=6,
                                           width=30)
        self.event_type_box.pack(side=tk.LEFT)
        self.event_period_box.pack(side=tk.LEFT)
        
        
        # self.period_monthly_rb = tk.Radiobutton(indicatoron=1,
                                          # master=self.event_type_frame,
                                          # text="Ежемесячно",
                                          # value=0,
                                          # variable=self.event_period_var
                                          # )
        # self.period_monthly_rb.pack(side=tk.LEFT)  # anchor=tk.W)
        # self.period_yearly_rb = tk.Radiobutton(indicatoron=1,
                                          # master=self.event_type_frame,
                                          # text="Ежегодно  ",
                                          # value=1,
                                          # variable=self.event_period_var
                                          # )
        # self.period_yearly_rb.pack(side=tk.RIGHT)  # anchor=W)
        
        self.options_frame.pack(padx=10,
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

        # EVENT_EDITOR_WINDOW_WIDTH = 400
        # EVENT_EDITOR_WINDOW_HEIGHT = 400
        self.update_idletasks()
                                
        
    
    def load_data(self):
        """Процедура загрузки данных в контролы."""
        self.load_event_types_list()
        event_name, event_date, self.event_type, self.event_period = self.database.get_event_data(self.id)
        # print("EVED.LD.EVNNM ", event_name)
        self.event_name_entry.insert(tk.END, event_name)
        # print("EVED.LD.EVNDT ", event_date)
        self.event_date_entry.set_date(event_date)
        # print("EVED.LD.EVNTP ", self.event_type)
        self.event_type_box.select_set(self.event_types_id_list.index(self.event_type))
        # self.event_type_box.focus(self.event_type)
        # print("EVED.LD.EVNPER ", self.event_period)
        self.event_period_box.select_set(self.event_types_id_list.index(self.event_period))
        # self.event_period_box.focus(self.event_period)

    
    def load_event_types_list(self):
        """Загружает список типов событий в listbox."""
        self.event_types_id_list, event_types_name_list = self.database.get_event_types_list()
        for event_name in event_types_name_list:
            self.event_type_box.insert(tk.END, event_name)
    
    def load_periods_list(self):
        """Загружает список периодов в listbox."""
        self.event_period_id_list, event_period_name_list = self.database.get_periods_list()
        for period in event_period_name_list:
            print("EVED:LPL:nam ", period)
            self.event_period_box.insert(tk.END, period)
        
    
    def save_data(self):
        """Сохраняет введённые данные."""
        event_date = datetime.strptime(self.event_date_entry.get(), "%d.%m.%Y")
        selected_type = self.event_type_box.curselection()
        # *** Если внезапно в листбоксе нет выбранного элемента - используем сохраненный ID
        if len(selected_type) == 0:
        
            print("*** Ooooopsss!....", self.event_type)
            event_type = self.event_type
        else:
            
            event_type = self.event_types_id_list[selected_type[0]]

        selected_period = self.event_period_box.curselection()
        # *** Если внезапно в листбоксе нет выбранного элемента - используем сохраненный ID
        if len(selected_period) == 0:
        
            print("*** Ooooopsss!....", self.event_period)
            event_period = self.event_period
        else:
            
            event_period = self.event_period_id_list[selected_period[0]]
            
        if self.id is None:

            self.database.insert_event(self.event_name_entry.get().strip(),
                                       event_date,
                                       event_type,
                                       self.event_period_var.get())
        else:

            self.database.update_event(self.id, 
                                       self.event_name_entry.get().strip(),
                                       event_date,
                                       event_type,
                                       self.event_period_var.get())
        print("EVED.LD.EVNPER ", self.event_period_var.get())
        self.destroy()
    
    
if __name__ == '__main__':
    root = tk.Tk()  
    event_editor = EventEditor(root)
    root.mainloop()
