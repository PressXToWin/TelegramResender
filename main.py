from telethon import events
from dotenv import load_dotenv
from settings import CHANNELS, KEYWORDS, MY_CHANNEL, client

load_dotenv()

client.start()


@client.on(events.NewMessage(CHANNELS))
async def handler(event):
    print(event.message.message)

    for keyword in KEYWORDS:
        if keyword in event.message.message:
            await client.forward_messages(MY_CHANNEL, event.message)
            break

client.run_until_disconnected()
