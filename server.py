import asyncio
import websockets
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import json
import ast
import threading

import serial
import time
arduinoPort='/dev/ttyACM0'
arduino = serial.Serial(port=arduinoPort, baudrate=115200, timeout=.1)

string_to_send = ""
old=""

def timer():
    global string_to_send
    global old
    if not string_to_send ==old:
        print("Received message from client: ", string_to_send)
        arduino.write((string_to_send+"\n").encode())

    old=string_to_send
    threading.Thread(target=timer).start()


timer()
# Generate a random encryption key and IV
encryption_key = get_random_bytes(32)
iv = get_random_bytes(16)


async def receive_messages(websocket, path):
    global arduino
    global arduinoPort
    
    
    global string_to_send
    # Send encryption key and iv to client
    message = {
        "encryptionKey": encryption_key.hex(),
        "iv": iv.hex()
    }
    await websocket.send(json.dumps(message))

    # Handle incoming messages
    async for encrypted_message in websocket:
        decrypted_message = None
        try:
            cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
            decrypted_message = cipher.decrypt(base64.b64decode(
                encrypted_message)).decode('utf-8').rstrip()
        except ValueError:
            print("Unable to decrypt message.")
        if decrypted_message:
            string_to_send = decrypted_message.split(']')[0][1:]
            # print("Received message: ", string_to_send)



async def start_server():
    async with websockets.serve(receive_messages, "localhost", 3000):
        await asyncio.Future()  # run forever

asyncio.run(start_server())
