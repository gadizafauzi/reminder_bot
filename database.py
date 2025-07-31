import sqlite3

def init_db():
    conn = sqlite3.connect('jadwal.db')
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
    conn = sqlite3.connect('jadwal.db')
    c = conn.cursor()
    c.execute(
        "INSERT INTO jadwal (user_id, waktu, pesan) VALUES (?, ?, ?)",
        (user_id, waktu, pesan)
    )
    conn.commit()
    conn.close()

def ambil_semua_jadwal():
    conn = sqlite3.connect('jadwal.db')
    c = conn.cursor()
    c.execute("SELECT * FROM jadwal")
    hasil = c.fetchall()
    conn.close()
    return hasil

def tambah_jadwal_default(user_id):
    # tiga kali sehari
    jadwals = [
        ("Everyday 07:00", "Ohayou! Saatnya belajar Bahasa Inggris~ 💬 Hafalin 10 kosa kata baru hari ini. Ganbare! 💪 *Dattebayo!*"),
        ("Everyday 13:00", "Konnichiwa Gadiza~ Jangan lupa semangat belajar Bahasa Inggrisnya yaa...! Power up! 💫📘 *Yoshaa!*"),
        ("Everyday 20.00", "Konbanwa~ waktunya review 📖⚔️ Hafalkan lagi 10 kosa kata. Ikuzooo!! 🔥 *Shinzou wo Sasageyo!*")

    ]
    for waktu, pesan in jadwals:
        tambah_jadwal(user_id, waktu, pesan)

        
