from StockGudang.style.Styles import *
from tkinter import messagebox

class UpdatePage(Frame):
    def refreshpage(self):
        self.refresher()

    def __init__(root, *args, **kwargs):
        conn = kwargs['db']
        Frame.__init__(root, *args, **kwargs)

        c = conn.cursor()

        def refresh():
            fetchGudang()
            newgudang.delete(0, END)
            newbarang.delete(0, END)
            newsatuan.delete(0, END)

            satuan.configure(state=NORMAL)
            satuan.delete(0, END)
            satuan.configure(state=DISABLED)
            msgtxt.set("")

        root.refresher = refresh

        def updatedata(data):
            c.execute("""
                UPDATE gudang
                SET `Nama Gudang` = :newgudang,
                    `Nama Barang` = :newbarang,
                    `Satuan` = :newsatuan
                WHERE `Nama Barang` = :barang
                """,
                data
            )
            c.execute("""
                UPDATE barang
                SET `Nama Barang` = :newbarang
                WHERE `Nama Barang` = :barang
                """,
                data
            )
            conn.commit()
            return True

        def submitForm():
            data = {
                'gudang': gudang.get(),
                'barang': barang.get(),
                'satuan': satuan.get(),
                'newgudang': newgudang.get(),
                'newbarang': newbarang.get(),
                'newsatuan': newsatuan.get()
            }
            if data['gudang'] == "Pilih gudang":
                msgtxt.set("Gudang perlu dipilih")
                return
            if data['barang'] == "Pilih barang":
                msgtxt.set("Barang perlu dipilih")
                return
            if data['newgudang'] == "":
                msgtxt.set("Nama gudang baru perlu diisi")
                return
            if data['newbarang'] == "":
                msgtxt.set("Nama barang baru perlu diisi")
                return
            if data['newsatuan'] == "":
                msgtxt.set("Satuan baru perlu diisi")
                return
            msgtxt.set("")
            try:
                updatedata(data)
                messagebox.showinfo("Success","Barang berhasil di update!")
                refresh()
            except Exception:
                messagebox.showerror("Error","Terjadi kesalahan saat update nama barang")

        def fetchGudang():
            c.execute("""
                SELECT DISTINCT `Nama Gudang` FROM gudang
            """)
            listGudang = [x[0] for x in c.fetchall()]
            gudang['values'] = listGudang
            gudang.set("Pilih gudang")
            barang['values'] = []
            barang.set("Pilih barang")

        def fetchBarang(selectGudang):
            gudang = selectGudang.widget.get()
            c.execute("""
            SELECT DISTINCT `Nama Barang` FROM gudang
            WHERE `Nama Gudang`=:gudang
            """,{
            'gudang' : gudang
            })
            listBarang = [x[0] for x in c.fetchall()]
            barang['values'] = listBarang
            newgudang.delete(0, END)
            newgudang.insert(0, gudang)

        def fetchSatuan(selectBarang):
            barang = selectBarang.widget.get()
            c.execute("""
                SELECT `Satuan` FROM gudang
                WHERE `Nama Barang`=:barang
            """,
                {
                    "barang":barang
                }
            )
            res = c.fetchone()
            newbarang.delete(0, END)
            newbarang.insert(0, barang)
            newsatuan.delete(0, END)
            newsatuan.insert(0, res[0])
            satuan.configure(state=NORMAL)
            satuan.delete(0, END)
            satuan.insert(0, res[0])
            satuan.configure(state=DISABLED)

        TitleLabel(root, text="Update").pack()

        master = Frame(root)
        form = Frame(master)

        FormLabel(form, text="Nama Gudang")
        gudang = ttk.Combobox(form, width=17, state="readonly")
        gudang.bind("<<ComboboxSelected>>", fetchBarang)
        FormInput(gudang)

        FormLabel(form, text="Nama Barang")
        barang = ttk.Combobox(form, width=17, state="readonly")
        barang.bind("<<ComboboxSelected>>", fetchSatuan)
        FormInput(barang)

        FormLabel(form, text="Satuan")
        satuan = Entry(form)
        FormInput(satuan)

        fetchGudang()
        form.grid(row=0, column=0)
        newform = Frame(master)

        FormLabel(newform, text="to")
        newgudang = Entry(newform)
        FormInput(newgudang)

        FormLabel(newform, text="to")
        newbarang = Entry(newform)
        FormInput(newbarang)

        FormLabel(newform, text="to")
        newsatuan = Entry(newform)
        FormInput(newsatuan)

        newform.grid(row=0, column=1)
        master.pack()

        ttk.Button(root, text="Update", command=submitForm).pack(pady=(20,0))

        msgtxt = StringVar()
        Label(root, textvariable=msgtxt, fg="red", bg=bgcolor, pady=10).pack()
