from style.Styles import *
from tkinter import messagebox

class DeletePage(Frame):
    def refreshpage(self):
        self.refresher()

    def __init__(root, *args, **kwargs):
        conn = kwargs['db']
        Frame.__init__(root, *args, **kwargs)

        c = conn.cursor()

        def refresh():
            fetchGudang()
            msgtxt.set("")

        root.refresher = refresh

        def deletedata(data):
            c.execute("""
                DELETE FROM gudang
                WHERE `Nama Gudang` = :gudang AND
                    `Nama Barang` = :barang
                """,
                data
            )
            conn.commit()

        def submitForm():
            data = {
                'gudang': gudang.get(),
                'barang': barang.get()
            }
            if data['gudang'] == "Pilih gudang":
                msgtxt.set("Gudang perlu dipilih")
                return
            if data['barang'] == "Pilih barang":
                msgtxt.set("Barang perlu dipilih")
                return
            msgtxt.set("")
            res = messagebox.askokcancel("Delete",f"Delete {barang.get()}?")
            if not res:
                return
            try:
                deletedata(data)
                messagebox.showinfo("Success","Barang berhasil di hapus!")
                refresh()
            except Exception:
                messagebox.showerror("Error","Terjadi kesalahan saat menghapus barang")

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
        

        TitleLabel(root, text="Delete").pack()
        form = Frame(root)

        FormLabel(form, text="Nama Gudang")
        gudang = ttk.Combobox(form, width=17, state="readonly")
        gudang.bind("<<ComboboxSelected>>", fetchBarang)
        FormInput(gudang)

        FormLabel(form, text="Nama Barang")
        barang = ttk.Combobox(form, width=17, state="readonly")
        FormInput(barang)

        fetchGudang()
        form.pack()
        
        ttk.Button(root, text="Delete", command=submitForm).pack(pady=(20,0))

        msgtxt = StringVar()
        Label(root, textvariable=msgtxt, fg="red", bg=bgcolor, pady=10).pack()
