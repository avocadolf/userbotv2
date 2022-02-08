"""
Author:         DerPatayaner
Date:           03.02.2022
Last change:    08.02.2022

This script mirrors from one to another channel

usage: userbot.py [-h] api_id api_hash [  history

"""
from telethon import TelegramClient, events
from telethon.tl.custom.message import Message
from telethon.tl.patched import MessageService
from pathlib import Path
import asyncio
import argparse 
import logging
import time
import json
import random

parser = argparse.ArgumentParser()

parser.add_argument('api_id', type=int, help='Telegram API ID')
parser.add_argument('api_hash', help='Telegram API Hash')

args = parser.parse_args()
api_id = args.api_id
api_hash = args.api_hash

client = TelegramClient("userbot.session", api_id, api_hash)
client.start()

loop = asyncio.get_event_loop()

channel_mapping = {}
ids = []


@client.on(events.NewMessage())
async def new_message_event(event):
    """Mirror all new Messages, except from MessageService events to another channel"""

    if event.message.chat.id in ids:
        chat_id = event.message.chat.id
        mirror_id = int(channel_mapping[str(chat_id)])
        to_entity = await client.get_input_entity(mirror_id)
        if isinstance(event.message, Message) and not isinstance(event.message, MessageService):
            await event.forward_to(to_entity)

def load_config():
    """Load config.json into channel_mapping dictonary"""

    global channel_mapping
    global ids
    my_file = Path("config.json")
    if not my_file.is_file():
        logging.error("Config file does not exist")
    js = None
    with open("config.json") as f:
        js = json.load(f)
    if js:
        channel_mapping = js["channel_mapping"]
        ids = [*channel_mapping]
        ids = [int(str) for str in ids] 

if __name__ == "__main__":
    load_config()
    client.run_until_disconnected()