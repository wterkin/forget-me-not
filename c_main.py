    #!/usr/bin/python3
# -*- coding: utf-8 -*-
#https://github.com/wterkin/forget-me-not.git
#https://younglinux.info/tkinter/bind.php

from tkinter.ttk  import Style
import tkinter as tk
from pathlib import Path
from datetime import datetime
import datetime as dtime
import c_config as cfg
import c_constants as cnst
import c_database as db
import c_eventlist as evlst
import c_tools as tls

# ############ Добавить в выборку справочник типов событий
# ############ Написать функцию конвертации тапля в список для выборки ежегодных событий
# Доработать окно редактирования событий с целью внедрения единовременных событий
# Добавить выборку для событий единовременных

class MainWindow(tk.Frame):
    def __init__(self, pmaster=None, **kwargs):
        """Конструктор."""
        self.__master = pmaster
        tk.Frame.__init__(self, self.__master, **kwargs) # background = "white"
        self.config = cfg.CConfiguration()
        self.database = db.CDatabase(self.config)
        if not self.is_database_exists():
        
            self.database.create_database()
            
        self.construct_window()
        self.load_data()


    def is_database_exists(self):
        """Проверяет наличие базы данных по пути в конфигурации."""
        config_folder_path = Path(self.config.restore_value(cfg.DATABASE_FILE_KEY))
        return config_folder_path.exists()
            
        
    def construct_window(self):
        """Создает интерфейс окна."""
        self.__master.title(cnst.MAIN_WINDOW_TITLE)
        self.style = Style()
        self.style.theme_use("default")
        #self.pack(fill=BOTH, expand=1)
        self.pack()
        
        # *** Тулбар
        self.toolbar_frame = tk.Frame(self.__master)
        self.event_list_button = tk.Button(self.toolbar_frame, text="Список событий", command=self.event_list)
        self.event_list_button.pack(side=tk.LEFT)
        self.quit_button = tk.Button(self.toolbar_frame, text="Выйти", command=self.quit_program)
        self.quit_button.pack(side=tk.RIGHT)
        self.toolbar_frame.pack(side=tk.TOP)
        
        # *** Текстовый бокс событий годовой периодичности.
        self.yearly_text_frame = tk.Frame(self.__master)
        self.yearly_text = tk.Text(self.yearly_text_frame, width=25, height=15, bg="Seashell")
        self.yearly_text.pack(fill=tk.BOTH)
        self.yearly_scroll_bar = tk.Scrollbar(command=self.yearly_text.yview)
        self.yearly_scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
        self.yearly_text.config(yscrollcommand=self.yearly_scroll_bar.set)
        self.yearly_text_frame.pack(expand=1, fill=tk.BOTH)

        # *** Текстовый бокс событий месячной периодичности.
        self.monthly_text_frame = tk.Frame(self.__master)
        self.monthly_text = tk.Text(self.monthly_text_frame, width=25, height=15, bg="Seashell")
        self.monthly_text.pack(fill=tk.BOTH)
        self.monthly_scroll_bar = tk.Scrollbar(command=self.monthly_text.yview)
        self.monthly_scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
        self.monthly_text.config(yscrollcommand=self.monthly_scroll_bar.set)
        self.monthly_text_frame.pack(expand=1, fill=tk.BOTH)
        
        
        # *** Отцентрируем окно
        window_left, window_top = tls.center_window(self.__master, cnst.MAIN_WINDOW_WIDTH, cnst.MAIN_WINDOW_HEIGHT)
        window_geometry = f"{cnst.MAIN_WINDOW_WIDTH}x{cnst.MAIN_WINDOW_HEIGHT}+{window_left}+{window_top}"
        self.__master.geometry(window_geometry)

        self.__master.update_idletasks()
       
       
    def get_master(self):
        """Возвращает мастера"""
        return self.__master


    def event_list(self):
        """Создает и открывает окно списка событий."""
        evlst.EventList(pmaster=self, pdatabase=self.database)


       
       
    def load_data(self):
        """Получает список событий за интервал, определенный в конфиге и отображает их."""
        def sort_list(x):
            
            print("@@@ ", x[3], x[2], x[1])
            xdate=dtime.date(x[3], x[2], x[1])
            print("### ", xdate)
            delta=xdate-dtime.date(2000,1,1)
            # ydate=dtime.datetime(y[3], y[2], y[1])
            print("!!! ", delta.days)
            return delta.days

        db_month_data = self.database.get_actual_monthly_events()
        # print("**** LDDT:month")
        # for event in db_month_data:

            # print(event)
        db_year_data = self.database.get_actual_yearly_events()
        # print("**** LDDT:year")
        # for event in db_year_data:

            # print(event)
            
        db_one_shot_data = self.database.get_actual_one_shot_events()
        # print("**** LDDT:one shot")
        # for event in db_one_shot_data:

            # print(event)
            
        full_data = []
        full_data.extend(db_one_shot_data)
        full_data.extend(db_year_data)
        full_data.extend(db_month_data)
        sorted(full_data, key=sort_list)
        # full_data.sort(key=sort_list)
        for event in full_data:

            print(event)
       
        
    def quit_program(self):
        """Закрывает программу."""
        self.config.write_config()
        self.quit()

        
def main():
    """Запускающая процедура."""
    # print("*** MAIN:MAIN:1 ", datetime.now())
    root = tk.Tk()
    main_window = MainWindow(root)
    main_window.pack()
    # print("*** MAIN:MAIN:2 ", datetime.now())
    root.mainloop()
 
 
if __name__ == '__main__':
    main()    
    
