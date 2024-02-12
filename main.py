from telethon import TelegramClient, events
import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

MY_CHANNEL = os.getenv("MY_CHANNEL")
KEYWORDS = os.getenv('KEYWORDS', '').split()
CHANNELS = os.getenv("CHANNELS").split()

if os.getenv('PROXY_IP', None):
    proxy = (os.getenv("PROXY_PROTO"), os.getenv("PROXY_IP"), os.getenv("PROXY_PORT"))
    client = TelegramClient('session', API_ID, API_HASH, proxy=proxy)
else:
    client = TelegramClient('session', API_ID, API_HASH)

client.start()


@client.on(events.NewMessage(CHANNELS))
async def handler(event):
    print(event.message.message)

    for keyword in KEYWORDS:
        if keyword in event.message.message:
            await client.forward_messages(MY_CHANNEL, event.message)
            break

client.run_until_disconnected()
