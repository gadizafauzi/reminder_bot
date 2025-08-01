import os
from telegram.ext import Updater, CommandHandler
from database import init_db, tambah_jadwal_default
from scheduler import kirim_pengingat, kirim_kosakata, kirim_review

# Ambil dari Railway ENV
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = int(os.environ.get("CHAT_ID"))

def start(update, context):
    update.message.reply_text("Reminder Bot aktif! Bot akan mengirim pesan dan kosakata otomatis 3x sehari. 🚀")

def main():
    init_db()
    tambah_jadwal_default(CHAT_ID)  # Untuk motivasi saja
    kirim_pengingat(TOKEN, CHAT_ID) # Sekarang butuh CHAT_ID juga
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
