import os
import requests
import threading
from flask import Flask
import telebot

# ۱. دریافت متغیرهای محیطی
BOT_TOKEN = os.getenv("YOUSEF_BOT_TOKEN", "").strip()
BASE_URL = os.getenv("BASE_URL", "").strip()
API_KEY = os.getenv("API_KEY", "").strip()

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# صفحه اصلی وب برای تایید سلامت پورت در رندر
@app.route('/')
def home():
    return "Bot is Running on Render!"

# دستور استارت ربات
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "ربات هوش مصنوعی فعال شد. پیام خود را بفرستید.")

# دریافت پیام‌ها و ارسال به Bluesminds
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": message.text}]
        }
        
        clean_url = BASE_URL if BASE_URL else "https://api.bluesminds.ir"
        response = requests.post(f"{clean_url}/v1/chat/completions", json=data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            reply = result['choices'][0]['message']['content']
            bot.reply_to(message, reply)
        else:
            bot.reply_to(message, f"خطا در ارتباط با سرور هوش مصنوعی: {response.status_code}")
    except Exception as e:
        bot.reply_to(message, f"یک خطای فنی رخ داد: {str(e)}")

# تابع مخصوص اجرای ربات تلگرام در Thread جداگانه
def run_telegram_bot():
    print("Starting Telegram Bot Polling...")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)

if __name__ == "__main__":
    # روشن کردن ربات در پس‌زمینه بدون بلاک کردن سرور وب
    t = threading.Thread(target=run_telegram_bot)
    t.daemon = True
    t.start()
    
    # روشن کردن وب‌سرور فلاسك روی پورت رندر
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
