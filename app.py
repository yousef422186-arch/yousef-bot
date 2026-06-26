import os
import requests
from flask import Flask, request
import telebot

BOT_TOKEN = os.getenv("YOUSEF_BOT_TOKEN", "").strip()
BASE_URL = os.getenv("BASE_URL", "").strip()
API_KEY = os.getenv("API_KEY", "").strip()

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "سلام یوسف عزیز! ربات هوش مصنوعی شما روی سرور رندر با موفقیت فعال شد. پیام خود را بفرستید.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY if API_KEY else BOT_TOKEN}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": message.text}]
        }
        
        clean_url = BASE_URL if BASE_URL else "https://bluesminds.com"
        response = requests.post(f"{clean_url}/v1/chat/completions", json=data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            reply_text = result['choices'][0]['message']['content']
            bot.reply_to(message, reply_text)
        else:
            bot.reply_to(message, f"خطا در ارتباط با سرور هوش مصنوعی. کد: {response.status_code}")
    except Exception as e:
        bot.reply_to(message, f"خطا: {str(e)}")

@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def home():
    return "Bot is Running on Render!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
