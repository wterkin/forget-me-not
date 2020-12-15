    #!/usr/bin/python3
# -*- coding: utf-8 -*-
#https://github.com/wterkin/forget-me-not.git
#https://younglinux.info/tkinter/bind.php

from tkinter.ttk  import Style
import tkinter as tk
from pathlib import Path


import c_config as cfg
import c_constants as cnst
import c_database as db
import c_eventlist as evlst
import c_tools as tls


class MainWindow(tk.Frame):
    def __init__(self, pmaster=None, **kwargs):
        """Конструктор."""
        self.master = pmaster
        tk.Frame.__init__(self, self.master, **kwargs) # background = "white"
        self.config = cfg.CConfiguration()
        self.database = db.CDatabase(self.config)
        if not self.is_database_exists():
        
            self.database.create_database()
            
        self.construct_window()


    def is_database_exists(self):
        """Проверяет наличие базы данных по пути в конфигурации."""
        config_folder_path = Path(self.config.restore_value(cfg.DATABASE_FILE_KEY))
        return config_folder_path.exists()
            
        
    def construct_window(self):
        """Создает интерфейс окна."""
        self.master.title(cnst.MAIN_WINDOW_TITLE)
        self.style = Style()
        self.style.theme_use("default")
        #self.pack(fill=BOTH, expand=1)
        self.pack()
        
        # *** Тулбар
        self.toolbar_frame = tk.Frame(self.master)
        self.event_list_button = tk.Button(self.toolbar_frame, text="Список событий", command=self.event_list)
        self.event_list_button.pack(side=tk.LEFT)
        self.quit_button = tk.Button(self.toolbar_frame, text="Выйти", command=self.quit_program)
        self.quit_button.pack(side=tk.RIGHT)
        self.toolbar_frame.pack(side=tk.TOP)
        
        # *** Текстовый бокс.
        self.text_frame = tk.Frame(self.master)
        self.text = tk.Text(self.text_frame, bg="Seashell")
        self.text.pack(fill=tk.BOTH)
        self.scroll_bar = tk.Scrollbar(command=self.text.yview)
        self.scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.config(yscrollcommand=self.scroll_bar.set)
        self.text_frame.pack(expand=1, fill=tk.BOTH)
        
        # *** Отцентрируем окно
        window_left, window_top = tls.center_window(self.master, cnst.MAIN_WINDOW_WIDTH, cnst.MAIN_WINDOW_HEIGHT)
        window_geometry = f"{cnst.MAIN_WINDOW_WIDTH}x{cnst.MAIN_WINDOW_HEIGHT}+{window_left}+{window_top}"
        self.master.geometry(window_geometry)

        self.master.update_idletasks()
       

    def event_list(self):
        """Создает и открывает окно списка событий."""
        evlst.EventList(pmaster=self, pdatabase=self.database)
        
        
    def quit_program(self):
        """Закрывает программу."""
        self.config.write_config()
        self.quit()

        
def main():
    """Запускающая процедура."""
    root = tk.Tk()
    main_window = MainWindow(root)
    main_window.pack()
    root.mainloop()
 
 
if __name__ == '__main__':
    main()    
    
