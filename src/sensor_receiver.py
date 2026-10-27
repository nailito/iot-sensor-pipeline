import pandas as pd
from pathlib import Path
import json
import time
import paho.mqtt.client as mqtt
from datetime import datetime, timezone
import math

HOST = "127.0.0.1" #local IP
PORT = 1883 #usual port without encryption

client_receiver = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    protocol=mqtt.MQTTv311,
)

def on_message(client,userdata,message):
    text = message.payload.decode("utf-8")
    data = json.loads(text)

    valid_data,error = validate_message(data)

    if error is not None:
        print("Message rejected:", error)
        return

    print("Message received:")
    print(valid_data)


def validate_message(data):
    set_sensor = {"event_id","sensor_id","event_time","value","unit"}
    if not set(data).issubset(set_sensor):
        return None, "missing_field(s)"

    if data["sensor_id"] != "Sensor_1":
        return None, "unexpected_sensor"
    
    try:
        date = datetime.strptime(data["event_time"], "%Y-%m-%d %H:%M:%S")
        if date.strftime("%Y-%m-%d %H:%M:%S") != data["event_time"]:
            return None, "date_format_missmatch"
    except (TypeError, ValueError):
        return None, "date_format_missmatch"
    
    value = data["value"]
    if type(value) not in (int, float) or not math.isfinite(value):
        return None, "value_missmatch"
    
    if data["unit"] not in ("°C", "%"):
        return None, "unite_missmatch"
    
    if data["unit"] == "%" and not 0 <= value <= 100:
        return None, "humidite_value_missmatch"
    else:
        print("message valide")
        return data, None
    
def on_subscribe(client, userdata, mid, reason_codes, properties):
    if reason_codes and all(not code.is_failure for code in reason_codes):
        print("Subscription confirmed.")
    else:
        print("Subscription refused:", reason_codes)

client_receiver.on_message = on_message
client_receiver.connect(HOST, PORT, keepalive=60)
client_receiver.loop_start()
limit = time.monotonic() + 5
while not client_receiver.is_connected():
    if time.monotonic() >= limit:
        raise TimeoutError("Connection to Mosquitto failed.")
    time.sleep(0.05)
print("Connection to Mosquitto succeded")

client_receiver.on_subscribe = on_subscribe
client_receiver.subscribe("sensors/kitchen", qos=1)

try:
    while True:
        time.sleep(1)
finally:
    client_receiver.disconnect()
    client_receiver.loop_stop()
