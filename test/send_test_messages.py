import json
import paho.mqtt.client as mqtt
import time


HOST = "127.0.0.1" #local IP
PORT = 1883 #usual port without encryption
QOS = 1

client_test = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    protocol=mqtt.MQTTv311,
)

client_test.connect(HOST, PORT, keepalive=60)
client_test.loop_start()

limit = time.monotonic() + 5

while not client_test.is_connected():
    if time.monotonic() >= limit:
        raise TimeoutError("Connection to Mosquitto failed.")
    time.sleep(0.05)

print("Connection to Mosquitto succeded")


humidity_wrong = {
    "event_id": "Sensor_1:humidity:2016-01-11 17:00:00",
    "sensor_id": "Sensor_1",
    "event_time": "2016-01-11 17:00:00",
    "value": 150,
    "unit": "%"
}

humidity_payload = json.dumps(humidity_wrong)

info = client_test.publish(
    topic="sensors/kitchen",
    payload=humidity_payload,
    qos=QOS,
    retain=False,
)

if info.rc != mqtt.MQTT_ERR_SUCCESS:
    #We chose to compare with MQTT.MQTT_ERR_SUCCESS (=0) for readability reasons.
    raise RuntimeError(f"Publication Request Rejected : {info.rc}")

info.wait_for_publish(timeout=5)

if not info.is_published():
    raise TimeoutError("No confirmation from the broker.")

print("Publication confirmed:", humidity_payload)
