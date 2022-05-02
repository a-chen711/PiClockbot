#Testing functionality of Telethon package

import configparser
import json
import asyncio
from datetime import date, datetime
import time
# from Telegram_Test import run

from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (
    PeerChannel
)


# you can get telegram development credentials in telegram API Development Tools
api_id = "API ID"
api_hash = "API HASH"

# use full phone number including + and country code
phone = "PHONE #"
username = "Username"

# Create the client and connect
client = TelegramClient(username, api_id, api_hash)
alex_ind = -1
nicole_ind = -1

@client.on(events.NewMessage(chats = "chat or channel name"))
async def my_event_handler(event):
    print(event.raw_text)
    if 'Trigger text' == event.raw_text:
        print("DETECTED1")
    elif 'Trigger text' == event.raw_text:
        print("DETECTED2")
client.start()
client.run_until_disconnected()