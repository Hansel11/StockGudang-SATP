import sqlite3
from datetime import date

db = "./data/stock.db"
conn = sqlite3.connect(db)
c = conn.cursor()

def user():
    c.execute("""
        CREATE TABLE user (
            'Name' text,
            'Pass' text
        )
    """)

def purge():
    c.execute("""
        DROP TABLE user
    """)

def altre():
    c.execute("""
        CREATE TABLE gudang (
            'Nama Gudang' text,
            'Nama Barang' text,
            'Saldo' integer,
            'Satuan' text
        )
    """)
    c.execute("""
        CREATE TABLE barang (
            'Nama Barang' text,
            'Saldo Awal' integer,
            'Pembelian' integer,
            'Pemakaian' integer,
            'Retur' integer,
            'Saldo Akhir' integer,
            'Tanggal' timestamp,
            'Nama User' text,
            'Nama Pemohon' text
        )
    """)

def newinsert():
    c.execute("""
        INSERT INTO gudang (
            'Nama Gudang',
            'Nama Barang',
            'Saldo',
            'Satuan'
        )
        VALUES(?, ?, ?, ?)
        """,
        (
            "Pakaian",
            "Baju",
            100,
            "pcs"
        )
    )
    conn.commit()
    c.execute("""
        INSERT INTO barang (
            'Nama Barang',
            'Saldo Awal',
            'Pembelian',
            'Pemakaian',
            'Retur',
            'Saldo Akhir',
            'Tanggal',
            'Nama User',
            'Nama Pemohon'
        )
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "Baju",
            90,
            10,
            0,
            0,
            100,
            date.today(),
            "bruh",
            "pogger",
        )
    )
    conn.commit()

def delete():
    c.execute("""
        DROP TABLE gudang
    """)
    c.execute("""
        DROP TABLE barang
    """)

def select():
    c.execute("""
        SELECT *
        FROM  gudang
    """)
    z = c.fetchall()
    for x in z:
        print(x)
    c.execute("""
        SELECT *
        FROM barang
    """)
    z = c.fetchall()
    for x in z:
        print(x)
        
def join():
    c.execute("""
        SELECT
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
    """)
    z = c.fetchall()
    for x in z:
        print(x)
        
if __name__ == '__main__':
    # purge()
    # user()
    # altre()
    # newinsert()
    # delete()
    # join()
    # select()
    print("success")

conn.close()