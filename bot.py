import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters
import re
from dotenv import load_dotenv
import os

BASE_URL = os.getenv("BASE_URL")

load_dotenv()

def is_only_link(text):
    pattern = r'^(https?://[^\s]+)$'
    return bool(re.match(pattern, text))

async def handle_message(update: Update, context):
    message = update.message

    if message.text:
        print("Received a text message:", message.text)

        type = ""

        if is_only_link(message.text):
            type = "LINK"

        url = f"{BASE_URL}/save?content={message.text}&type={type}"

        print(f"Link to be requested: {url}")

        try:
            response = requests.post(url)
            response.raise_for_status()
            
            await update.message.reply_text(f"Saved! Check it on {BASE_URL}")
        except requests.exceptions.RequestException as e:
            await update.message.reply_text(f"Error: {e}")

    elif message.photo:
        print("Received a photo message.", message.photo)

    elif message.audio:
        print("Received an audio message.", message.audio)

    elif message.document:
        print("Received a document message.", message.document)

if __name__ == "__main__":
    application = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    application.run_polling()
