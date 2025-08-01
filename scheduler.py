from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from telegram import Bot
from database import ambil_semua_jadwal
import pytz, json, random, os

def kirim_pengingat(bot_token, chat_id):
    tz = pytz.timezone('Asia/Jakarta')
    scheduler = BackgroundScheduler(timezone=tz)
    bot = Bot(token=bot_token)

    # 🔁 Motivasi tiap menit
    def cek_jadwal():
        now_str = datetime.now(tz).strftime('Everyday %H:%M')
        for _id, user_id, waktu, pesan in ambil_semua_jadwal():
            if waktu == now_str:
                try:
                    bot.send_message(chat_id=user_id, text=f"⏰ Waktunya belajar!\n📚 {pesan}")
                except Exception as e:
                    print(f"Gagal kirim ke {user_id}: {e}")

    scheduler.add_job(cek_jadwal, 'interval', minutes=1)

    # 🧠 Kosakata pagi
    scheduler.add_job(lambda: kirim_kosakata(bot_token, chat_id, 15, "Pagi"), 'cron', hour=7, minute=0)

    # 🧠 Kosakata siang
    scheduler.add_job(lambda: kirim_kosakata(bot_token, chat_id, 15, "Siang"), 'cron', hour=13, minute=0)

    # 🔁 Review malam
    scheduler.add_job(lambda: kirim_review(bot_token, chat_id), 'cron', hour=19, minute=0)

    scheduler.start()

def kirim_kosakata(bot_token, chat_id, jumlah, sesi):
    bot = Bot(token=bot_token)
    with open("vocab_list.json", "r", encoding="utf-8") as f:
        all_vocab = json.load(f)

    today = datetime.now().strftime("%Y-%m-%d")
    sent_file = "sent_words_today.json"

    if os.path.exists(sent_file):
        with open(sent_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        if data.get("date") != today:
            data = {"date": today, "words": []}
    else:
        data = {"date": today, "words": []}

    sent_words = data["words"]
    already_sent = [w["word"] for w in sent_words]
    remaining = [v for v in all_vocab if v["word"] not in already_sent]
    selected = random.sample(remaining, min(jumlah, len(remaining)))

    data["words"].extend(selected)
    with open(sent_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    pesan = f"📚 *Kosakata Sesi {sesi}* ({jumlah} kata)\n\n"
    for i, v in enumerate(selected, 1):
        pesan += f"{i}. *{v['word']}* — {v['meaning']}\n"

    bot.send_message(chat_id=chat_id, text=pesan, parse_mode="Markdown")

def kirim_review(bot_token, chat_id):
    bot = Bot(token=bot_token)
    sent_file = "sent_words_today.json"
    if not os.path.exists(sent_file): return

    with open(sent_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not data.get("words"): return

    pesan = "🌙 *Review Kosakata Hari Ini* (30 kata)\n\n"
    for i, v in enumerate(data["words"], 1):
        pesan += f"{i}. *{v['word']}* — {v['meaning']}\n"

    bot.send_message(chat_id=chat_id, text=pesan, parse_mode="Markdown")
