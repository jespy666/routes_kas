#!/usr/bin/env python3

import tkinter as tk
import json



def get_date():
    date_year = date.get()
    date_year.split('/')



win = tk.Tk()
win.geometry(f'240x260+100+200')
win['bg'] = '#3761E8'
win.title('Routes calculator')
date = tk.Entry(win)
date.grid(row=0, column=0)
tk.Button(text='Month/Year:mm/yyyy', command=get_date).grid(row=1, column=0)
win.mainloop()
