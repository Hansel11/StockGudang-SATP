from tkinter import Menu, PhotoImage, Tk, messagebox
from StockGudang.style.Styles import bgcolor
# from ttkthemes import ThemedStyle

from StockGudang.LoginPage import LoginPage
from StockGudang.InsertPage import InsertPage
from StockGudang.CreatePage import CreatePage
from StockGudang.UpdatePage import UpdatePage
from StockGudang.DeletePage import DeletePage
from StockGudang.ExportPage import ExportPage
from StockGudang.RegisterPage import RegisterPage

import sqlite3

db = "./StockGudang/data/stock.db"
conn = sqlite3.connect(db)

def switchpage(target):
    if target == switchpage.curr:
        return
    pages[target].refreshpage(root)
    pages[target].tkraise()
    switchpage.curr = target

def logout():
    res = messagebox.askokcancel("Logout","Are you sure?")
    if not res:
        return
    root.config(menu=loginmenu)
    switchpage("LoginPage")

def login():
    root.config(menu=mymenu)
    switchpage("InsertPage")

if __name__ == '__main__':

    root = Tk()
    root.withdraw()
    root.title("Stock Gudang")
    root.geometry("500x500")
    root.configure(bg=bgcolor)
    root.iconphoto(False, PhotoImage(file='./StockGudang/asset/SATP-1.png'))
    # style = ThemedStyle(root)
    # style.theme_use('arc')

    mymenu = Menu(root)
    manage = Menu(mymenu, tearoff=0)
    account = Menu(mymenu, tearoff=0)
    mymenu.add_command(label="Home", command=lambda: switchpage("InsertPage"))
    mymenu.add_cascade(label="Manage", menu=manage)
    manage.add_command(label="Create", command=lambda: switchpage("CreatePage"))
    manage.add_command(label="Update", command=lambda: switchpage("UpdatePage"))
    manage.add_command(label="Delete", command=lambda: switchpage("DeletePage"))
    mymenu.add_command(label="Export", command=lambda: switchpage("ExportPage"))
    mymenu.add_cascade(label="Account", menu=account)
    account.add_command(label="Logout", command=lambda: logout())

    loginmenu = Menu(root)
    loginmenu.add_command(label="Login", command=lambda: switchpage("LoginPage"))
    loginmenu.add_command(label="Register", command=lambda: switchpage("RegisterPage"))

    root.config(menu=loginmenu)
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    
    pages = {}

    for page in (InsertPage, CreatePage, UpdatePage, DeletePage, ExportPage, RegisterPage):
        page_name = page.__name__
        pages[page_name] = page(root, db=conn)
        pages[page_name].grid(row=0, column=0, sticky="nsew")

    
    pages["LoginPage"] = LoginPage(root, controller=login, db=conn)
    pages["LoginPage"].grid(row=0, column=0, sticky="nsew")
    pages["LoginPage"].refreshpage(root)
    switchpage.curr = "LoginPage"

    root.deiconify()
    root.mainloop()

conn.commit()
conn.close()
