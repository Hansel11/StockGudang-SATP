from style.Styles import *
from tkinter import messagebox

class CreatePage(Frame):
    def refreshpage(self):
        self.refresher()

    def __init__(root, *args, **kwargs):
        conn = kwargs['db']
        Frame.__init__(root, *args, **kwargs)

        c = conn.cursor()

        def refresh():
            fetchgudang()
            barang.delete(0, END)
            awal.delete(0, END)
            satuan.delete(0, END)
            msgtxt.set("")

        root.refresher = refresh

        def savebarang(data):
            c.execute("""
                    INSERT INTO gudang (
                        'Nama Gudang',
                        'Nama Barang',
                        'Saldo',
                        'Satuan'
                    )
                    VALUES(:gudang, :barang, :saldo, :satuan)
                    """,
                data
            )

        def submitForm():
            data = {
                'gudang': gudang.get(),
                'barang': barang.get(),
                'saldo': int(awal.get()),
                'satuan': satuan.get()
            }
            if data['gudang'] == "":
                msgtxt.set("Nama gudang harus diisi")
                return
            if data['barang'] == "Pilih gudang":
                msgtxt.set("Pilih gudang atau tambahkan gudang baru")
                return
            if data['barang'] == "":
                msgtxt.set("Nama barang perlu diisi")
                return
            if data['awal'] == "":
                msgtxt.set("Saldo awal perlu diisi")
                return
            try:
                data['awal'] = int(data['awal'])
            except Exception:
                msgtxt.set("Saldo harus berupa bilangan bulat")
                return
            if data['satuan'] == "":
                msgtxt.set("Satuan perlu diisi")
                return
            c.execute("""
                SELECT `Nama Barang` FROM gudang
                WHERE `Nama Barang` = :barang
            """,data)
            if c.fetchall():
                msgtxt.set("Barang sudah terdaftar")
                return
            msgtxt.set("")
            try:
                savebarang(data)
                messagebox.showinfo("Success","Barang berhasil ditambahkan!")
                refresh()
            except Exception:
                messagebox.showerror("Error","Terjadi kesalahan saat menambahkan barang")

        def fetchgudang():
            c.execute("""
                SELECT DISTINCT `Nama Gudang` FROM gudang
            """)
            listGudang = [x[0] for x in c.fetchall()]
            gudang['values'] = listGudang
            gudang.set("Pilih gudang")

        TitleLabel(root, text="Create").pack()
        form = Frame(root)

        FormLabel(form, text="Nama Gudang")
        gudang = ttk.Combobox(form, width=17)
        FormInput(gudang)

        FormLabel(form, text="", pady=1)
        note = Label(form, text="Note: ketik untuk menambahkan gudang baru" ,fg="gray", font=("Helvetica 9 italic"))
        FormInput(note)

        FormLabel(form, text="Nama Barang")
        barang = Entry(form)
        FormInput(barang)

        FormLabel(form, text="Saldo Awal")
        awal = Entry(form)
        FormInput(awal)

        FormLabel(form, text="Satuan")
        satuan = Entry(form)
        FormInput(satuan)

        fetchgudang()
        form.pack()

        ttk.Button(root, text="Create", command=submitForm).pack(pady=(20,0))

        msgtxt = StringVar()
        Label(root, textvariable=msgtxt, fg="red", bg=bgcolor, pady=10).pack()
