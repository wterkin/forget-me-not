#!/usr/bin/python3
# -*- coding: utf-8 -*-
#https://github.com/wterkin/forget-me-not.git
#https://younglinux.info/tkinter/bind.php
#from tkinter import *
from tkinter.ttk  import Style
import tkinter as tk
#import pathlib
from pathlib import Path

import config as cfg
import database as db
import eventeditor as eved
import eventlist as evlst

MAIN_WINDOW_TITLE = "Forget-Me-Not version 0,1"
MAIN_WINDOW_WIDTH = 640 
MAIN_WINDOW_HEIGHT = 480

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
        self.centerWindow()
        
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
 
        self.text_frame.pack(expand=1, fill=tk.BOTH)
        
        
    def centerWindow(self):
        """Центрирует окно относительно экрана."""
        #w = root.winfo_screenwidth()
        #h = root.winfo_screenheight()

        li_window_width = MAIN_WINDOW_WIDTH
        li_window_height = MAIN_WINDOW_HEIGHT
        li_screen_width = self.master.winfo_screenwidth()
        li_screen_height = self.master.winfo_screenheight()
        li_left = (li_screen_width - li_window_width) / 2
        li_top = (li_screen_height - li_window_height) / 2
        self.master.geometry('%dx%d+%d+%d' % (li_window_width, li_window_height, li_left, li_top))


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
    
