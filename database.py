import sqlite3

DB_NAME = "jadwal.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS jadwal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            waktu TEXT,
            pesan TEXT
        )
    ''')
    conn.commit()
    conn.close()

def tambah_jadwal(user_id, waktu, pesan):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "INSERT INTO jadwal (user_id, waktu, pesan) VALUES (?, ?, ?)",
        (user_id, waktu, pesan)
    )
    conn.commit()
    conn.close()

def ambil_semua_jadwal():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM jadwal")
    hasil = c.fetchall()
    conn.close()
    return hasil

def tambah_jadwal_default(user_id):
    jadwals = [
        ("Everyday 07:00", "Ohayou! Gadiza, yuk langsung hafalin 15 kosa kata Bahasa Inggris. Ganbatte! *Dattebayo!*"),
        ("Everyday 13:00", "Konnichiwa! Lanjut lagi hafalan 15 kosa kata baru ya, Gadiza. Ikuzo! *Yoshaa!*"),
        ("Everyday 20:00", "Konbanwa. Saatnya review 30 kosa kata hari ini. Tetap semangat belajar, Gadiza! Ganbatte! *Shinzou wo Sasageyo!*")
    ]
    for waktu, pesan in jadwals:
        tambah_jadwal(user_id, waktu, pesan)
