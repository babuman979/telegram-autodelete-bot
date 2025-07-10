from flask import Flask
from threading import Thread
from telethon import TelegramClient, events
import logging

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=10000)

Thread(target=run).start()

logging.basicConfig(level=logging.INFO)

api_id = 24753135
api_hash = '52811df3777abd38394499b1e3060448'
bot_token = '7995114209:AAEWRCYLeq0Ck8F8NaVPQ-KqYLBRrudn158'
channel_username = 'shoppingwithusonline'

client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(chats=channel_username))
async def handler(event):
    if not event.message.media:
        await event.delete()
        print("Deleted non-media message.")

client.run_until_disconnected()
