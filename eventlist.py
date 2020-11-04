#!/usr/bin/python
# -*- coding: utf-8 -*-

import tkinter as tk

import database as db
import eventeditor as eved



class EventList(tk.Toplevel):
    """Класс окна списка событий."""
    def __init__(self, pmaster, pdatabase, **kwargs):
        """Конструктор."""
        tk.Toplevel.__init__(self, pmaster, **kwargs)
        self.master = pmaster
        self.database = pdatabase
        self.construct_window()
        self.load_data()
        # *** Показываем окно
        self.transient(self.master)
        self.grab_set()
        self.master.wait_window(self)

   
    def construct_window(self):
        """Создает интерфейс окна."""
        # *** Фрейм кнопок
        self.list_buttons_frame = tk.Frame(self)
        self.add_button = tk.Button(command=self.insert_event,
                                    master=self.list_buttons_frame,
                                    text="Добавить")
        self.add_button.pack(side=tk.LEFT)
        self.edit_button = tk.Button(command=self.update_event,
                                     master=self.list_buttons_frame,
                                     text="Редактировать")
        self.edit_button.pack(side=tk.LEFT)  # tk.RIGHT)
        self.delete_button = tk.Button(command=self.delete_event,
                                       master=self.list_buttons_frame,
                                       text="Удалить")
        self.delete_button.pack(side=tk.LEFT)  # tk.RIGHT)
        self.close_button = tk.Button(command=self.destroy,
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

   

    def delete_event(self):
        """Удаляет выбранное событие."""
        pass

    
    def insert_event(self):
        """Добавляет новое событие в базу."""
        event_editor = eved.EventEditor(self,
                                        pdatabase=self.database,
                                        pid=None)


    def load_data(self):
        """Обновляет данные в списке."""
        self.event_id_list, self.event_name_list = self.database.get_events_list()
        for name in self.event_name_list:
            self.events_box.insert(tk.END, name)


    def update_event(self):
        """Изменяет уже существующее событие."""
        pass

    
if __name__ == '__main__':
    master = tk.Tk()
    event_list = EventList(master)
    master.mainloop()
