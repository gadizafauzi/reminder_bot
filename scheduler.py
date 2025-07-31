from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from telegram import Bot
from database import ambil_semua_jadwal
import pytz

def kirim_pengingat(bot_token):
    tz = pytz.timezone('Asia/Jakarta')
    scheduler = BackgroundScheduler(timezone=tz)
    bot = Bot(token=bot_token)

    def cek_jadwal():
        now_str = datetime.now(tz).strftime('Everyday %H:%M')
        for _id, user_id, waktu, pesan in ambil_semua_jadwal():
            if waktu == now_str:
                try:
                    bot.send_message(chat_id=user_id, text=f"⏰ Waktunya belajar!\n📚 {pesan}")
                except Exception as e:
                    print(f"Gagal kirim ke {user_id}: {e}")

    scheduler.add_job(cek_jadwal, 'interval', minutes=1)
    scheduler.start()
