from telegram.ext import Updater, CommandHandler
from database import init_db, tambah_jadwal_default
from scheduler import kirim_pengingat

# — GANTI sesuai token dan chat ID kamu —
TOKEN   = "8033179513:AAEkMmYb2Cg4muFj2eZAIAdNFAmHtWmoVxE"
CHAT_ID = 1484327026

def start(update, context):
    update.message.reply_text("Reminder Bot aktif! Pesan akan dikirim otomatis sesuai jadwal 😊")

def main():
    # 1. Inisialisasi DB
    init_db()

    # 2. Tambah jadwal default (pagi/siang/malam)
    tambah_jadwal_default(CHAT_ID)

    # 3. Start background scheduler
    kirim_pengingat(TOKEN)

    # 4. Usual polling handlers (opsional: user bisa tambah jadwal manual)
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
