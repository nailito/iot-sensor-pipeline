import pandas as pd
from pathlib import Path
import json
import time
import paho.mqtt.client as mqtt

HOST = "127.0.0.1" #local IP
PORT = 1883 #usual port without encryption

client_receiver = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    protocol=mqtt.MQTTv311,
)

client_receiver.connect(HOST, PORT, keepalive=60)
client_receiver.loop_start()
limit = time.monotonic() + 5
while not client_receiver.is_connected():
    if time.monotonic() >= limit:
        raise TimeoutError("Connection to Mosquitto failed.")
    time.sleep(0.05)
print("Connection to Mosquitto succeded")

 
    