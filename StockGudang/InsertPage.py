from tkinter import messagebox
from datetime import datetime

from StockGudang.style.Styles import *

class InsertPage(Frame):
    # def refreshpage(self, *args):
    #     self.destroy()
    #     self.__init__(self, *args, db=self.db)

    def refreshpage(self):
        self.refresher()

    def __init__(root, *args, **kwargs):
        conn = kwargs['db']
        root.db = conn
        Frame.__init__(root, *args, **kwargs)

        saldo = {
            "awal" : 0,
            "beli" : 0,
            "pakai" : 0,
            "ret" : 0,
            "akhir" : 0,
            "sat" : ""
        }
        satuans = []

        c = conn.cursor()

        def refresh():
            fetchGudang()
            pembelian.delete(0, END)
            pemakaian.delete(0, END)
            retur.delete(0, END)
            awal.configure(state=NORMAL)
            awal.delete(0, END)
            awal.configure(state=DISABLED)
            pembelian.configure(state=DISABLED)
            pemakaian.configure(state=DISABLED)
            retur.configure(state=DISABLED)
            akhir.configure(state=NORMAL)
            akhir.delete(0, END)
            akhir.configure(state=DISABLED)
            pemohon.delete(0, END)
            for satuan in satuans:
                satuan.grid_forget()
            satuans.clear()
            msgtxt.set("")

        root.refresher = refresh

        def updateSaldo(**kwargs):
            kw = [*kwargs.keys()][0]
            try:
                saldo[kw] = int(kwargs[kw].get())
            except Exception:
                saldo[kw] = 0
            res = saldo['awal'] + saldo['beli'] - saldo['pakai'] - saldo['ret']
            saldo['akhir'] = res
            akhir.configure(state=NORMAL)
            akhir.delete(0, END)
            akhir.insert(0,res)
            akhir.configure(state=DISABLED)

        def savechanges(data):
            c.execute("""
                INSERT INTO barang
                VALUES(:barang,
                        :awal,
                        :beli,
                        :pakai,
                        :ret,
                        :akhir,
                        :date,
                        :user,
                        :pemohon
                    )
                """,
                data
            )
            c.execute("""
                UPDATE gudang
                SET `Saldo` = :akhir
                WHERE `Nama Barang` = :barang
                """,
                data
            )
            conn.commit()

        def confirmchanges():
            data = {
                'gudang' : gudang.get(),
                'barang': barang.get(),
                'date': datetime.now(),
                'user': User.name,
                'pemohon': pemohon.get()
            }
            data.update(saldo)
            if data['gudang'] == "Pilih gudang":
                msgtxt.set("Gudang perlu dipilih")
                return
            if data['barang'] == "Pilih barang":
                msgtxt.set("Barang perlu dipilih")
                return
            if data['beli'] == "" and data['pakai'] == "" and data['ret'] == "":
                msgtxt.set("Pembelian, Pemakaian, atau Retur perlu diisi")
                return
            if data["akhir"] < 0:
                msgtxt.set("Saldo tidak mencukupi pemakaian")
                return
            if data['pemohon'] == "":
                msgtxt.set("Nama Pemohon perlu diisi")
                return
            msgtxt.set("")
            try:
                savechanges(data)
                messagebox.showinfo("Success","Data berhasil dimasukkan")
                refresh()
            except Exception:
                messagebox.showerror("Error","Terjadi kesalahan saat memasukan data")

        def fetchGudang():
            c.execute(
                """SELECT DISTINCT `Nama Gudang` FROM gudang"""
                )
            listGudang = [x[0] for x in c.fetchall()]
            gudang['values'] = listGudang
            gudang.set("Pilih gudang")
            barang['values'] = []
            barang.set("Pilih barang")

        def fetchBarang(selectGudang):
            gdg = selectGudang.widget.get()
            c.execute("""
            SELECT DISTINCT `Nama Barang` FROM gudang
            WHERE `Nama Gudang`=:gudang
            """,{
            'gudang' : gdg
            })
            listBarang = [x[0] for x in c.fetchall()]
            barang['values'] = listBarang
            barang.set("Pilih barang")
            
        def fetchAwal(selectBarang):
            try:
                brg = selectBarang.widget.get()
            except:
                brg = selectBarang.get()
            c.execute("""
                SELECT `Saldo`, `Satuan` FROM gudang
                WHERE `Nama Barang`=:barang
            """,
                {
                    "barang":brg
                }
            )
            res = c.fetchone()
            saldo["awal"] = res[0]
            saldo["sat"] = res[1]
            awal.configure(state=NORMAL)
            awal.delete(0, END)
            awal.insert(0, res[0])
            awal.configure(state=DISABLED)
            pembelian.configure(state=NORMAL)
            pemakaian.configure(state=NORMAL)
            retur.configure(state=NORMAL)
            row = awal.grid_info()['row']
            for i in range(row,row+5):
                lab = Label(form, text=res[1])
                satuans.append(lab)
                lab.grid(row=i, column=2)
            
        # Title
        TitleLabel(root, text="Stock Gudang").pack()
        form = Frame(root)

        # Gudang
        FormLabel(form, text="Nama Gudang")
        gudang = ttk.Combobox(form, width=17, state="readonly")
        gudang.bind("<<ComboboxSelected>>", fetchBarang)
        FormInput(gudang)
        
        # Barang
        FormLabel(form, text="Nama Barang")
        barang = ttk.Combobox(form, width=17, state="readonly")
        barang.bind("<<ComboboxSelected>>", fetchAwal)
        FormInput(barang)

        # Awal
        FormLabel(form, text="Saldo awal")
        awal = ttk.Entry(form, state=DISABLED)
        FormInput(awal)

        # Pembelian
        vPembelian = StringVar()
        vPembelian.trace("w", lambda name, index, mode, sv=vPembelian: updateSaldo(beli=sv))
        FormLabel(form, text="Pembelian")
        pembelian = Entry(form, textvariable=vPembelian, state=DISABLED)
        FormInput(pembelian)
        
        # Pemakaian
        vPemakaian = StringVar()
        vPemakaian.trace("w", lambda name, index, mode, sv=vPemakaian: updateSaldo(pakai=sv))
        FormLabel(form, text="Pemakaian")
        pemakaian = Entry(form, textvariable=vPemakaian, state=DISABLED)
        FormInput(pemakaian)

        # Retur
        vRetur = StringVar()
        vRetur.trace("w", lambda name, index, mode, sv=vRetur: updateSaldo(ret=sv))
        FormLabel(form, text="Retur")
        retur = Entry(form, textvariable=vRetur, state=DISABLED)
        FormInput(retur)

        # Akhir
        FormLabel(form, text="Saldo akhir")
        akhir = Entry(form, state=DISABLED)
        FormInput(akhir)

        # Pemohon
        FormLabel(form, text="Nama Pemohon")
        pemohon = Entry(form)
        FormInput(pemohon)
        
        fetchGudang()
        form.pack()

        ttk.Button(root, text="Confirm",command=confirmchanges).pack(pady=(20,0))

        msgtxt = StringVar()
        Label(root, textvariable=msgtxt, fg="red", bg=bgcolor, pady=10).pack()
