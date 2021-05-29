from tkinter import *
import tkinter.ttk as ttk

bgcolor = "#151E29"

class User:
    name = ""

class Frame(Frame):
    def __init__(self, *args, bg=bgcolor, **kwargs):
        try:
            kwargs.pop('db')
        except Exception:
            pass
        super(Frame, self).__init__(*args, bg=bg,  **kwargs)

class Entry(ttk.Entry):
    def __init__(self, *args, **kwargs):
        super(Entry, self).__init__(*args, **kwargs)

class Label(Label):
    def __init__(self, *args, fg="white", bg=bgcolor, **kwargs):
        super(Label, self).__init__(*args, fg=fg, bg=bg, **kwargs)
    
class TitleLabel(Label):
    def __init__(self, *args, pady=15, fontsize=18, **kwargs):
        super(TitleLabel, self).__init__(*args, **kwargs, pady=pady, font=('Trebuchet MS',fontsize,'bold'))

class FormLabel(Label):
    __counter__ = 0
    def __init__(self, *args, pady=5, **kwargs):
        super(FormLabel, self).__init__(*args, **kwargs, pady=pady, padx=10)
        self.grid(row=FormLabel.__counter__, column=0, sticky="W")
        FormLabel.__counter__ += 1

def FormInput(item):
    item.grid(row=FormInput.counter, column=1, sticky="W")
    FormInput.counter += 1
FormInput.counter = 0
