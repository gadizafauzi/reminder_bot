import os
from telegram.ext import Updater, CommandHandler
from database import init_db, tambah_jadwal_default
from scheduler import kirim_pengingat

# Ambil dari environment variable Railway
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = int(os.environ.get("CHAT_ID"))  # pastikan jadi int

def start(update, context):
    update.message.reply_text("Reminder Bot aktif! Pesan akan dikirim otomatis sesuai jadwal 😊")

def main():
    # 1. Inisialisasi DB
    init_db()

    # 2. Tambah jadwal default (pagi/siang/malam) ke user (1x saja, bisa diberi kondisi kalau perlu)
    tambah_jadwal_default(CHAT_ID)

    # 3. Jalankan scheduler background
    kirim_pengingat(TOKEN)

    # 4. Jalankan polling untuk command /start (opsional)
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
