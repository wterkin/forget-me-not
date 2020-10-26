#!/usr/bin/python
# -*- coding: utf-8 -*-
 
from tkinter import Tk, Frame, BOTH


MAIN_WINDOW_TITLE = "Forget-Me-Not version 0,1"
MAIN_WINDOW_WIDTH = 290
MAIN_WINDOW_HEIGHT = 150

class MainWindow(Frame):
    
    def __init__(self, po_parent):
        Frame.__init__(self, po_parent) # background = "white"
        self.parent = po_parent
        self.parent.title(MAIN_WINDOW_TITLE)
        self.pack(fill=BOTH, expand=1)
        self.centerWindow()


    def centerWindow(self):
        li_window_width = MAIN_WINDOW_WIDTH
        li_window_height = MAIN_WINDOW_HEIGHT
        li_screen_width = self.parent.winfo_screenwidth()
        li_screen_height = self.parent.winfo_screenheight()
        li_left = (li_screen_width - li_window_width) / 2
        li_top = (li_screen_height - li_window_height) / 2
        self.parent.geometry('%dx%d+%d+%d' % (li_window_width, li_window_height, li_left, li_top))

        

def main():
    application = Tk()
    main_window = MainWindow(application)
    application.mainloop()
 
if __name__ == '__main__':
    main()    
    
