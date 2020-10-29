#!/usr/bin/python
# -*- coding: utf-8 -*-
from tkinter import *

class EventEditor(Frame):
    def __init__(self, root):
        Frame.__init__(self, root) # background = "white"
        #super().__init__(root)
        self.event_name_frame = Frame(root)
        self.event_name_entry = Entry(self.event_name_frame, width=20)
        self.event_name_entry.pack(side=RIGHT)
        self.event_name_label = Label(self.event_name_frame, width=20, text="Название события")  #  bg='black', fg='white', )
        self.event_name_label.pack(side=LEFT)
        self.event_name_frame.pack(padx=10, pady=10)

        self.event_type_frame = Frame(root)
        #self.event_type_var = IntVar()
        #self.event_type_var.set(1)
        #self.memory_day_rb = Radiobutton(indicatoron=1,
                                         #master=self.event_type_frame,
                                         #text=" День памяти   ",
                                         #value=0,
                                         #variable=self.event_type_var
                                         #)
        #self.memory_day_rb.pack(anchor=W)
        #self.birth_day_rb = Radiobutton(indicatoron=1,
                                        #master=self.event_type_frame,
                                        #text=" День рождения ",
                                        #value=1,
                                        #variable=self.event_type_var
                                        #)
        #self.birth_day_rb.pack(anchor=W)
        #self.memory_date_rb = Radiobutton(indicatoron=1,
                                          #master=self.event_type_frame,
                                          #text=" Памятная дата ",
                                          #value=2,
                                          #variable=self.event_type_var
                                          #)
        #self.memory_date_rb.pack(anchor=W)
        #self.reminder_date_rb = Radiobutton(indicatoron=1,
                                            #master=self.event_type_frame,
                                            #text=" Напоминание   ",
                                            #value=3,
                                            #variable=self.event_type_var
                                            #)
        #self.reminder_date_rb.pack(anchor=W)
        #++++++++++++++++
        #self.some_flag = BooleanVar()
        #self.some_flag.set(1)
        #self.some_check = Checkbutton(self.event_type_frame,
                                      #text="Подтверждаю!",
                                      #variable=self.some_flag,
                                      #onvalue=1,
                                      #offvalue=0)
        #self.some_check.pack(anchor=W)
        #-----------------
        self.event_type_box = Listbox(self.event_type_frame, width=20, height=4)
        self.event_type_box.insert(0, "День памяти")
        self.event_type_box.insert(1, "День рождения")
        self.event_type_box.insert(2, "Памятная дата")
        self.event_type_box.insert(3, "Напоминание")
        self.event_type_box.pack()
        #self.event_type_box.curselection()
        self.event_type_frame.pack(padx=10, pady=10)
        

        
        
        #self.event_date_frame = Frame(root)
        
        self.buttons_frame = Frame(root)
        self.ok_button = Button(command=self.quit,
                                master=self.buttons_frame,
                                text="Принять")
        self.ok_button.pack(side=LEFT)
        self.cancel_button = Button(command=self.quit,
                                    master=self.buttons_frame,
                                    text="Отмена")
        self.cancel_button.pack(side=RIGHT)
        self.buttons_frame.pack(padx=10, pady=10)
        
    #b1['text'] = "Изменено"
    #b1['bg'] = '#000000'
    #b1['activebackground'] = '#555555'
    #b1['fg'] = '#ffffff'
    #b1['activeforeground'] = '#ffffff'
    #b1.config(command=change)
    #l1 = Label(text="Машинное обучение", font="Arial 32")
    #l2 = Label(text="Распознавание образов", font=("Comic Sans MS", 24, "bold"))
    #l1.config(bd=20, bg='#ffaaaa')
    #l2.config(bd=20, bg='#aaffff')
    #l1.pack()
    #l2.pack()
    #Label(text="Пункт выдачи").pack()
    #Button(text="Взять", command=take).pack()
    #lab = Label(width=10, height=1)
    #lab.pack()
if __name__ == '__main__':
    root = Tk()
    event_editor = EventEditor(root)
    root.mainloop()
