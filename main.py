# ==== Import required modules ====
from flask import Flask
from threading import Thread
from telethon import TelegramClient, events
import logging
import asyncio  # Needed for delay

# ==== Flask app for keeping bot alive ====
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=10000)

# Start Flask server in a separate thread
Thread(target=run).start()

# ==== Telegram API credentials ====
api_id = 24753135
api_hash = '52811df3777abd38394499b1e3060448'
bot_token = '7995114209:AAEWRCYLeq0Ck8F8NaVPQ-KqYLBRrudn158'
channel_username = 'shoppingwithusonline'  # No @ symbol

# ==== Set up logging ====
logging.basicConfig(level=logging.INFO)

# ==== Start Telethon client ====
client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

# ==== Store previous message ID ====
last_message_id = None

# ==== Event handler for new messages ====
@client.on(events.NewMessage(chats=channel_username))
async def handler(event):
    global last_message_id

    # Delay before deleting previous message
    if last_message_id:
        try:
            await asyncio.sleep(5)  # 🕒 Delay to appear human-like
            await client.delete_messages(channel_username, last_message_id)
            print(f"Deleted previous message ID: {last_message_id}")
        except Exception as e:
            print(f"Error deleting previous message: {e}")

    # If current message has no media, delete it
    if not event.message.media:
        await event.delete()
        print("Deleted non-media message.")
    else:
        # Save current media message ID
        last_message_id = event.message.id

# ==== Start listening to Telegram ====
client.run_until_disconnected()
