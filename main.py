from flask import Flask
from threading import Thread
from telethon import TelegramClient, events
import asyncio
import random
import logging

# === Flask app to keep bot alive ===
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

Thread(target=lambda: app.run(host='0.0.0.0', port=10000)).start()

# === Telegram credentials ===
api_id = 24753135
api_hash = '52811df3777abd38394499b1e3060448'
bot_token = '7995114209:AAEWRCYLeq0Ck8F8NaVPQ-KqYLBRrudn158'
channel_username = 'shoppingwithusonline'

# === Start Telethon client ===
client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

# === Lock to avoid overlapping deletions ===
deletion_lock = asyncio.Lock()

# === Retryable delete function ===
async def safe_delete(message, max_retries=3):
    for attempt in range(max_retries):
        try:
            await message.delete()
            print(f"✅ Deleted message ID: {message.id}")
            return True
        except Exception as e:
            print(f"⚠️ Attempt {attempt + 1} failed to delete {message.id}: {e}")
            await asyncio.sleep(1 + attempt)  # backoff
    print(f"❌ Failed to delete message ID: {message.id} after {max_retries} attempts")
    return False

# === Main handler ===
@client.on(events.NewMessage(chats=channel_username))
async def handler(event):
    async with deletion_lock:
        try:
            # === Handle non-media messages ===
            if not event.message.media:
                delay = random.uniform(2, 5)
                await asyncio.sleep(delay)
                await safe_delete(event.message)
                print(f"🗑️ Non-media message deleted after {delay:.1f}s delay.")
                return

            # === Media message: wait a few seconds for stability ===
            await asyncio.sleep(5)

            # === Fetch more messages to ensure full context ===
            messages = await client.get_messages(channel_username, limit=10)

            # === Delete all except the current media message ===
            for msg in messages:
                if msg.id != event.message.id:
                    await safe_delete(msg)

        except Exception as e:
            print(f"❌ Handler error: {e}")

# === Run bot ===
client.run_until_disconnected()
