from style.Styles import *
from PIL import ImageTk, Image
from tkinter import Label as TkLab, messagebox
import hashlib

class RegisterPage(Frame):
    def refreshpage(self):
        self.refresher()

    def __init__(root, *args, controller, **kwargs):
        conn = kwargs['db']
        c = conn.cursor()
        Frame.__init__(root, *args, **kwargs, bg=bgcolor)

        def refresh():
            name.delete(0,END)
            pw.delete(0,END)
            cpw.delete(0,END)
            msgtxt.set("")

        root.refresher = refresh

        def register(data):
            c.execute("""
                INSERT INTO user
                VALUES(:name, :pass)
            """, data)

        def confirmReg():
            data = {
                'name': name.get(),
                'pass': pw.get(),
                'cpass': cpw.get()
            }
            if data['name'] == "":
                msgtxt.set("Masukkan username")
                return
            if data['pass'] == "":
                msgtxt.set("Masukkan password")
                return
            if data['cpass'] == "":
                msgtxt.set("Konfirmasi password")
                return
            if data['pass'] != data['cpass']:
                msgtxt.set("Konfirmasi password salah")
                return
            c.execute("SELECT * FROM user WHERE `Name`=:name", data)
            if c.fetchone():
                msgtxt.set("Username sudah pernah terdaftar")
                return
            data['pass'] = hashlib.sha256(data['pass'].encode('utf-8')).hexdigest()
            msgtxt.set("") 
            print(str(data['pass']))
            try:
                register(data)
                messagebox.showinfo("Success","User berhasil terdaftar")
                refresh()
            except Exception:
                messagebox.showerror("Error","Register failed")

        header = Frame(root)
        img = Image.open('./asset/SATP-1.png').resize((75, 75), Image.ANTIALIAS)
        logo = ImageTk.PhotoImage(img)
        pic = TkLab(header, image=logo, bg=bgcolor)
        pic.photo = logo
        pic.grid(row=0, column=0)

        head = Label(header, text="SEKOLAH ASRAMA TARUNA PAPUA", font=("Sans Serif", 16, "bold"))
        head.grid(row=0, column=1)
        header.pack()

        TitleLabel(root, text="Register", fontsize=15).pack()

        formlogin = Frame(root)
        FormLabel(formlogin, text="Username")
        name = Entry(formlogin)
        FormInput(name)

        FormLabel(formlogin, text="Password")
        pw = Entry(formlogin, show="\u2022")
        FormInput(pw)
        formlogin.pack()

        FormLabel(formlogin, text="Confirm Password")
        cpw = Entry(formlogin, show="\u2022")
        FormInput(cpw)
        formlogin.pack()
        
        ttk.Button(root, text="Register", command=lambda: confirmReg()).pack(pady=(20,0))

        msgtxt = StringVar()
        Label(root, textvariable=msgtxt, fg="red", bg=bgcolor, pady=10).pack()

