from telethon import events
from dotenv import load_dotenv
from settings import client
from database.orm import add_message, get_channels

load_dotenv()

client.start()


@client.on(events.NewMessage(get_channels(None)))
async def handler(event):
    add_message(
        message_id=event.message.id,
        channel_id=event.message.chat_id,
        text=event.message.message,
        message_date=event.message.date
    )

if __name__ == '__main__':
    client.run_until_disconnected()
