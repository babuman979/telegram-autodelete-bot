from flask import Flask
from threading import Thread
from telethon import TelegramClient, events
import logging
import asyncio
import random  # 👈 For random delay

# === Flask app to keep alive ===
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=10000)

Thread(target=run).start()

# === Telegram credentials ===
api_id = 24753135
api_hash = '52811df3777abd38394499b1e3060448'
bot_token = '7995114209:AAEWRCYLeq0Ck8F8NaVPQ-KqYLBRrudn158'
channel_username = 'shoppingwithusonline'

# === Start Telethon bot ===
client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(chats=channel_username))
async def handler(event):
    # === Delete non-media messages with random delay ===
    if not event.message.media:
        delay = random.uniform(2, 5)  # 🕒 Delay between 2–5 seconds
        await asyncio.sleep(delay)
        await event.delete()
        print(f"Deleted non-media message after {delay:.1f}s delay.")
        return

    # === Wait before deleting older media posts ===
    await asyncio.sleep(5)

    try:
        # Get last 5 messages
        messages = await client.get_messages(channel_username, limit=5)

        # Delete all except the current one
        for msg in messages:
            if msg.id != event.message.id:
                await client.delete_messages(channel_username, msg.id)
                print(f"Deleted old message ID: {msg.id}")
    except Exception as e:
        print(f"Error cleaning up messages: {e}")

# === Start the bot ===
client.run_until_disconnected()
