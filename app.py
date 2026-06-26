import os
import requests
import io
import threading
from flask import Flask
import telebot
from PIL import Image

BOT_TOKEN = os.getenv("YOUSEF_BOT_TOKEN", "").strip()
API_KEY = os.getenv("API_KEY", "").strip()
BASE_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# تابع تولید عکس
def generate_image(prompt):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.post(BASE_URL, headers=headers, json={"inputs": prompt})
    if response.status_code == 200:
        return response.content
    return None

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "سلام! من ربات شما هستم.\nبرای چت بنویسید: /chat [متن]\nبرای تولید عکس بنویسید: /draw [توصیف عکس]")

@bot.message_handler(commands=['draw'])
def draw_command(message):
    prompt = message.text.replace('/draw', '').strip()
    if not prompt:
        bot.reply_to(message, "لطفاً توصیف عکس را بنویسید. مثال: /draw a cute cat")
        return
    
    bot.reply_to(message, "در حال کشیدن تصویر... لطفاً صبر کنید.")
    img_data = generate_image(prompt)
    if img_data:
        bot.send_photo(message.chat.id, io.BytesIO(img_data))
    else:
        bot.reply_to(message, "خطا در تولید تصویر!")

@bot.message_handler(commands=['chat'])
def chat_command(message):
    # کدهای چت متنی قبلی را می‌توانید اینجا دوباره اضافه کنید
    bot.reply_to(message, "این بخش در حال توسعه است.")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
