import os
import requests
import threading
from flask import Flask
import telebot

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
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        # استفاده از مدل فوق‌قدرتمند و محبوب که مخصوص چت است
        data = {
            "model": "meta-llama/Llama-3.1-8B-Instruct",
            "messages": [{"role": "user", "content": message.text}]
        }
            
        response = requests.post(f"{BASE_URL}/chat/completions", json=data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            reply = result['choices'][0]['message']['content']
            bot.reply_to(message, reply)
        else:
            bot.reply_to(message, f"خطای ارتباطی: {response.status_code}")
    except Exception as e:
        bot.reply_to(message, f"خطا: {str(e)}")

def run_telegram_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    t = threading.Thread(target=run_telegram_bot)
    t.start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
