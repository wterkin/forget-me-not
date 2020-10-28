#!/usr/bin/python
# -*- coding: utf-8 -*-
 
from tkinter import *
from tkinter.ttk  import Frame, Button, Style

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
        lo_quit_button = Button(self.toolbar_frame, text="Выйти", command=self.quit)
        lo_quit_button.pack(side=RIGHT)
        #lo_quit_button.place(x=50, y=50)
        self.toolbar_frame.pack(side=TOP)
        self.text_frame = Frame(self.parent)
        self.text = Text(self.text_frame)
        self.text.pack()
        self.text_frame.pack(expand=1, fill=BOTH)
        
    def centerWindow(self):
        li_window_width = MAIN_WINDOW_WIDTH
        li_window_height = MAIN_WINDOW_HEIGHT
        li_screen_width = self.parent.winfo_screenwidth()
        li_screen_height = self.parent.winfo_screenheight()
        li_left = (li_screen_width - li_window_width) / 2
        li_top = (li_screen_height - li_window_height) / 2
        self.parent.geometry('%dx%d+%d+%d' % (li_window_width, li_window_height, li_left, li_top))

        

def main():
    root = Tk()
    application = MainWindow(root)
    root.mainloop()
 
if __name__ == '__main__':
    main()    
    
