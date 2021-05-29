from tkinter import messagebox
from style.Styles import *
from tkcalendar import DateEntry
from tkinter.filedialog import asksaveasfilename
from xlsxwriter.workbook import Workbook

class DateEntry(DateEntry):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,
                        selectbackground='gray80',
                        selectforeground='black',
                        normalbackground='white',
                        normalforeground='black',
                        background='gray90',
                        foreground='black',
                        bordercolor='gray90',
                        othermonthforeground='gray50',
                        othermonthbackground='white',
                        othermonthweforeground='gray50',
                        othermonthwebackground='white',
                        weekendbackground='white',
                        weekendforeground='black',
                        headersbackground='white',
                        headersforeground='gray70',
                        **kwargs)

class ExportPage(Frame):
    def refreshpage(self):
        pass

    def __init__(root, *args, **kwargs):
        conn = kwargs['db']
        Frame.__init__(root, *args, **kwargs)

        # style = ttk.Style(root)
        # style.theme_use('clam')

        def export():
            data = {
                'start': start.get_date(),
                'end': end.get_date()
            }

            files = [('Microsoft Excel Worksheet', '*.xlsx'),
                    ('All Files', '*.*')]
            file = asksaveasfilename(initialfile=f"Export {data['start']} - {data['end']} .xlsx",
            filetypes = files, defaultextension=".xlsx")

            if file == "":
                return
 
            mysel=c.execute("""SELECT
                            a.`Nama Gudang`,
                            b.`Nama Barang`,
                            b.`Saldo Awal`,
                            b.`Pembelian`,
                            b.`Pemakaian`,
                            b.`Retur`,
                            b.`Saldo Akhir`,
                            a.`Satuan`,
                            b.`Tanggal`,
                            b.`Nama User`,
                            b.`Nama Pemohon`
                            FROM  gudang a JOIN barang b
                            ON a.'Nama Barang' = b.'Nama Barang'
                            WHERE
                            date(Tanggal) BETWEEN
                            date(:start) AND date(:end)
                            ORDER BY Tanggal
                            """, data)

            try:
                workbook = Workbook(file)
                worksheet = workbook.add_worksheet()
                bold = workbook.add_format({'bold': True, 'border': 1})
                border = workbook.add_format({'border': 1})
                
                for i, col in enumerate([description[0] for description in c.description]):
                    worksheet.write(0, i, col, bold)
                    worksheet.set_column(i, i, len(col)+2)
                for i, row in enumerate(mysel):
                    for j, value in enumerate(row):
                        worksheet.write(i+1, j, value, border)
                workbook.close()
                messagebox.showinfo("Success","Export Successful")
            except Exception:
                messagebox.showerror("Error","Export Failed")

        c=conn.cursor()
        TitleLabel(root, text="Export to Excel").pack()
        form = Frame(root)
        form.pack()

        FormLabel(form, text="Start Date")
        start = DateEntry(form)
        FormInput(start)

        FormLabel(form, text="End Date")
        end = DateEntry(form)
        FormInput(end)

        ttk.Button(root, text="Export", command=export).pack(pady=(20,0))
