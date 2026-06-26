import os
import requests
import threading
from flask import Flask
import telebot

# ۱. دریافت متغیرهای محیطی
BOT_TOKEN = os.getenv("YOUSEF_BOT_TOKEN", "").strip()
BASE_URL = "https://router.huggingface.co/v1"
API_KEY = os.getenv("API_KEY", "").strip()

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Running on Render!"

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        # استفاده از مدل استاندارد و ساده‌تر برای جلوگیری از ارور 400
        data = {
            "model": "meta-llama/Llama-3.1-8B-Instruct",
            "messages": [{"role": "user", "content": message.text}],
            "max_tokens": 500
        }
            
        response = requests.post(f"{BASE_URL}/chat/completions", json=data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            reply = result['choices'][0]['message']['content']
            bot.reply_to(message, reply)
        else:
            bot.reply_to(message, f"خطای سرور ({response.status_code}): {response.text[:100]}")
    except Exception as e:
        bot.reply_to(message, f"خطا: {str(e)}")

def run_telegram_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    t = threading.Thread(target=run_telegram_bot)
    t.start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
