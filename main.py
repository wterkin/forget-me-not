#!/usr/bin/python
# -*- coding: utf-8 -*-
#https://younglinux.info/tkinter/bind.php
from tkinter import *
from tkinter.ttk  import Frame, Button, Style

import eventeditor as eved
import eventlist as evlst
import config

MAIN_WINDOW_TITLE = "Forget-Me-Not version 0,1"
MAIN_WINDOW_WIDTH = 640 
MAIN_WINDOW_HEIGHT = 480

class MainWindow(Frame):
    
    def __init__(self, po_parent):
        """Конструктор."""
        Frame.__init__(self, po_parent) # background = "white"
        self.parent = po_parent
        self.construct_window()

    def construct_window(self):
        """Создает интерфейс окна."""
        self.parent.title(MAIN_WINDOW_TITLE)
        self.style = Style()
        self.style.theme_use("default")
        #self.pack(fill=BOTH, expand=1)
        self.pack()
        self.centerWindow()
        
        self.toolbar_frame = Frame(self.parent)
        self.event_list_button = Button(self.toolbar_frame, text="Список событий", command=self.event_list)
        self.event_list_button.pack(side=LEFT)
        self.quit_button = Button(self.toolbar_frame, text="Выйти", command=self.quit)
        self.quit_button.pack(side=RIGHT)
        self.toolbar_frame.pack(side=TOP)
        
        self.text_frame = Frame(self.parent)
        self.text = Text(self.text_frame)
        self.text.pack()
        self.scroll_bar = Scrollbar(command=self.text.yview)
        self.scroll_bar.pack(side=RIGHT, fill=Y)
        self.text.config(yscrollcommand=self.scroll_bar.set)
        #self.text.insert(1.0, "Hello world!\nline two")
 
        #self.text.tag_add('title', 1.0, '1.end')
        #self.text.tag_config('title', justify=CENTER,
                        #font=("Verdana", 24, 'bold'))
 
        self.text_frame.pack(expand=1, fill=BOTH)
        
    def centerWindow(self):
        li_window_width = MAIN_WINDOW_WIDTH
        li_window_height = MAIN_WINDOW_HEIGHT
        li_screen_width = self.parent.winfo_screenwidth()
        li_screen_height = self.parent.winfo_screenheight()
        li_left = (li_screen_width - li_window_width) / 2
        li_top = (li_screen_height - li_window_height) / 2
        self.parent.geometry('%dx%d+%d+%d' % (li_window_width, li_window_height, li_left, li_top))

    def event_list(self):
        event_list = evlst.EventList(self.parent)
        #print("****", event_editor)
        event_list.mainloop()
        #event_editor.grab_set()
        #event_editor = EventEditor(root)
        #root.mainloop()
        
        #window = eved.EventEditor(self.parent)
        #window.mainloop()
        
def main():
    root = Tk()
    application = MainWindow(root)
    root.mainloop()
 
if __name__ == '__main__':
    main()    
    
