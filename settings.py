import os

from dotenv import load_dotenv
from telethon import TelegramClient

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

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:////app/bot.db')

BOT_TOKEN = os.getenv('BOT_TOKEN')
