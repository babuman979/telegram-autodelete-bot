# ==== Imports ====
from flask import Flask
from threading import Thread
from telethon import TelegramClient, events
import logging

# ==== Flask Server for UptimeRobot Ping ====
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=10000)

Thread(target=run).start()

# ==== Telegram Bot Setup ====
logging.basicConfig(level=logging.INFO)

api_id = 24753135
api_hash = '52811df3777abd38394499b1e3060448'
bot_token = '7995114209:AAEWRCYLeq0Ck8F8NaVPQ-KqYLBRrudn158'
channel_username = 'shoppingwithusonline'  # Without @ or link

client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

# ==== Track Last Message ID ====
last_message_id = None

@client.on(events.NewMessage(chats=channel_username))
async def handler(event):
    global last_message_id

    # Delete previous message if available
    if last_message_id:
        try:
            await client.delete_messages(channel_username, last_message_id)
            print(f"Deleted previous message ID: {last_message_id}")
        except Exception as e:
            print(f"Error deleting previous message: {e}")

    # Delete current message if it has no media
    if not event.message.media:
        await event.delete()
        print("Deleted non-media message.")
    else:
        # Save current message ID if it's media
        last_message_id = event.message.id

# ==== Start Bot ====
client.run_until_disconnected()
