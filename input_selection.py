# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 13:19:16 2023

@author: Thomas Vouk
"""

import tkinter as tk
from tkinter import messagebox
from tkinter import *
import psycopg2
import sys


def input_selection(input_selection,name):
    root = tk.Tk()  # generate input object
    root.title("Plot configurations")
    root.geometry('650x300')

    # Create a Tkinter variable
    tkvar = tk.StringVar(root)

    # options
    choices = input_selection.keys()
    tkvar.set(name)  # set the default option

    def on_selection(value):
        global choice
        choice = value  # store the user's choice
        root.destroy()  # close window

    popupMenu = tk.OptionMenu(root, tkvar, *choices, command=on_selection)

    tk.Label(root, text="Input Parameters for calculation", width=85).grid(row=0, column=0)
    popupMenu.grid(row=1, column=0)
    
    popupMenu1 = tk.OptionMenu(root, tkvar, *choices, command=on_selection)

    popupMenu1.grid(row=1, column=0)
    

    root.mainloop()
    if input_selection[choice] == 'Stop': #If user choose "Stop" whole programm should stop
        sys.exit()
    return input_selection[choice]


def main():
    calculation_year={'2020':"'2020-01-01 00:00:00'",'2030':"'2030-01-01 00:00:00'",
                      '2040':"'2040-01-01 00:00:00'",'2050':"'2050-01-01 00:00:00'",
                      'Stop':"Stop"}
    
    ref_year={'2017':"'2017-01-01 00:00:00'",'2019':"'2019-01-01 00:00:00'",
              '2020':"'2020-01-01 00:00:00'",'2030':"'2030-01-01 00:00:00'",
              '2040':"'2040-01-01 00:00:00'",'2050':"'2050-01-01 00:00:00'",
              'Stop':"Stop"}
    
    
    
    print(input_selection(calculation_year,'Calculation year'))
    print(input_selection(ref_year,'Referenc year'))


if __name__ == '__main__':

    sys.exit(main())