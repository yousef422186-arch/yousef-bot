import os
import requests
import threading
from flask import Flask
import telebot

# تنظیمات محیطی
BOT_TOKEN = os.getenv("YOUSEF_BOT_TOKEN", "").strip()
API_KEY = os.getenv("API_KEY", "").strip()
BASE_URL = "https://router.huggingface.co/v1"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # ساخت درخواست برای هوش مصنوعی
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "meta-llama/Llama-3.1-8B-Instruct",
            "messages": [{"role": "user", "content": message.text}],
            "max_tokens": 500
        }
            
        # ارسال درخواست با مهلت زمانی (Timeout) برای جلوگیری از هنگ کردن
        response = requests.post(f"{BASE_URL}/chat/completions", json=data, headers=headers, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            reply = result['choices'][0]['message']['content']
            bot.reply_to(message, reply)
        else:
            bot.reply_to(message, f"خطای سرور ({response.status_code}): لطفاً لحظاتی دیگر تلاش کنید.")
            
    except Exception as e:
        bot.reply_to(message, f"خطای فنی: {str(e)}")

# اجرای همزمان ربات و وب‌سرور
def run_telegram_bot():
    print("Bot is polling...")
    bot.infinity_polling(none_stop=True)

if __name__ == "__main__":
    t = threading.Thread(target=run_telegram_bot)
    t.daemon = True
    t.start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
