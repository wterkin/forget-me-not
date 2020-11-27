#!/usr/bin/python3
# -*- coding: utf-8 -*-
#https://github.com/wterkin/forget-me-not.git
#https://younglinux.info/tkinter/bind.php
#from tkinter import *
from tkinter.ttk  import Style
import tkinter as tk
from pathlib import Path


import c_config as cfg
import c_database as db
import c_eventlist as evlst
import c_tools as tls


MAIN_WINDOW_TITLE = "Forget-Me-Not version 0,1"
MAIN_WINDOW_WIDTH = 800 
MAIN_WINDOW_HEIGHT = 600

class MainWindow(tk.Frame):
    def __init__(self, pmaster=None, **kwargs):
        """Конструктор."""
        self.master = pmaster
        tk.Frame.__init__(self, self.master, **kwargs) # background = "white"
        self.config = cfg.Configuration()
        self.database = db.CDatabase(self.config.restore_value(cfg.DATABASE_FILE_KEY))
        if not self.is_database_exists():
            self.database.create_database()
            
        self.construct_window()


    def is_database_exists(self):
        """Проверяет наличие базы данных по пути в конфигурации."""
        config_folder_path = Path(self.config.restore_value(cfg.DATABASE_FILE_KEY))
        return config_folder_path.exists()
            
        
    def construct_window(self):
        """Создает интерфейс окна."""
        self.master.title(MAIN_WINDOW_TITLE)
        self.style = Style()
        self.style.theme_use("default")
        #self.pack(fill=BOTH, expand=1)
        self.pack()
        
        self.toolbar_frame = tk.Frame(self.master)
        self.event_list_button = tk.Button(self.toolbar_frame, text="Список событий", command=self.event_list)
        self.event_list_button.pack(side=tk.LEFT)
        self.quit_button = tk.Button(self.toolbar_frame, text="Выйти", command=self.quit_program)
        self.quit_button.pack(side=tk.RIGHT)
        self.toolbar_frame.pack(side=tk.TOP)
        
        self.text_frame = tk.Frame(self.master)
        self.text = tk.Text(self.text_frame)
        self.text.pack()
        self.scroll_bar = tk.Scrollbar(command=self.text.yview)
        self.scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.config(yscrollcommand=self.scroll_bar.set)
        #self.text.insert(1.0, "Hello world!\nline two")
        #self.text.tag_add('title', 1.0, '1.end')
        #self.text.tag_config('title', justify=CENTER,
                        #font=("Verdana", 24, 'bold'))
        self.master.update_idletasks()
        self.text_frame.pack(expand=1, fill=tk.BOTH)
        # tls.set_window_size(self.master, MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)
        # print(f'{MAIN_WINDOW_WIDTH}x{MAIN_WINDOW_HEIGHT}')
        self.master.geometry(f'{MAIN_WINDOW_WIDTH}x{MAIN_WINDOW_HEIGHT}')
        # self.master.update()
        tls.center_window(self.master)
        self.master.update_idletasks()
        
        
    def centerWindow(self, window=None):
        """Центрирует окно относительно экрана."""
        if window is None:
            
            window = self.master
            li_window_width = MAIN_WINDOW_WIDTH
            li_window_height = MAIN_WINDOW_HEIGHT
        else:
            
            li_window_width, li_window_height = tls.get_window_size(window)

        li_screen_width = window.winfo_screenwidth()
        li_screen_height = window.winfo_screenheight()
        li_left = (li_screen_width - li_window_width) / 2
        li_top = (li_screen_height - li_window_height) / 2
        window.geometry('%dx%d+%d+%d' % (li_window_width, li_window_height, li_left, li_top))
        tls.get_window_size(window)


    def event_list(self):
        """Создает и открывает окно списка событий."""
        event_list = evlst.EventList(pmaster=self,
                                     pdatabase=self.database)
        
        
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
    
