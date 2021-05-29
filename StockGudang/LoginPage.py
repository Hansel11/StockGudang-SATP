from StockGudang.style.Styles import *
from PIL import ImageTk, Image
from tkinter import Label as TkLab, font
import hashlib

class LoginPage(Frame):
    def refreshpage(self):
        self.refresher()

    def __init__(root, *args, controller, **kwargs):
        conn = kwargs['db']
        c = conn.cursor()
        Frame.__init__(root, *args, **kwargs, bg=bgcolor)

        def refresh():
            name.delete(0,END)
            pw.delete(0,END)
            msgtxt.set("")

        root.refresher = refresh

        def confirmLogin():
            data = {
                'name': name.get(),
                'pass': pw.get(),
            }
            if data['name'] == "":
                msgtxt.set("Masukkan username")
                return
            if data['pass'] == "":
                msgtxt.set("Masukkan password")
                return
            c.execute("SELECT * FROM user WHERE `Name`=:name", data)
            res = c.fetchone()
            if not res:
                msgtxt.set("Username salah")
                return
            data['pass'] = hashlib.sha256(data['pass'].encode('utf-8')).hexdigest()
            if data['pass'] != res[1]:
                msgtxt.set("Password salah")
                return
            msgtxt.set("")
            User.name = data['name']
            controller()
        root.bind('<Return>', confirmLogin) 

        header = Frame(root)
        img = Image.open('./StockGudang/asset/SATP-1.png').resize((75, 75), Image.ANTIALIAS)
        logo = ImageTk.PhotoImage(img)
        pic = TkLab(header, image=logo, bg=bgcolor)
        pic.photo = logo
        pic.grid(row=0, column=0)

        head = Label(header, text="SEKOLAH ASRAMA TARUNA PAPUA", font=("Sans Serif", 16, "bold"))
        head.grid(row=0, column=1)
        header.pack()

        TitleLabel(root, text="Login", fontsize=15).pack()

        formlogin = Frame(root)
        FormLabel(formlogin, text="Username")
        name = Entry(formlogin)
        FormInput(name)

        FormLabel(formlogin, text="Password")
        pw = Entry(formlogin, show="\u2022")
        FormInput(pw)
        formlogin.pack()
        
        ttk.Button(root, text="Login", command=lambda: confirmLogin()).pack(pady=(20,0))

        msgtxt = StringVar()
        Label(root, textvariable=msgtxt, fg="red", bg=bgcolor, pady=10).pack()
