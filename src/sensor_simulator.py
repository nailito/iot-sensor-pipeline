import pandas as pd
from pathlib import Path
import json
import time
import paho.mqtt.client as mqtt

project_dir = Path(__file__).resolve().parent.parent
file = project_dir / "data" / "energydata_complete.csv"

df_raw = pd.read_csv(file)

df = df_raw[["date", "T1", "RH_1"]].copy()
df = df.sort_values("date")

messages = []

for index, raw_data in df.head(5).iterrows():
    temperature_message = {"event_id": f"Sensor_1:temperature:{raw_data['date']}",
               "sensor_id":"Sensor_1",
               "event_time":raw_data["date"],
               "value":raw_data["T1"],
               "unit":"°C"}
    humidity_message = {"event_id": f"Sensor_1:humidity:{raw_data['date']}",
               "sensor_id":"Sensor_1",
               "event_time":raw_data["date"],
               "value":raw_data["RH_1"],
               "unit":"%"}
    temperature_payload = json.dumps(temperature_message,ensure_ascii=False)  #ascii=False because we have ° for the temp
    humidity_payload = json.dumps(humidity_message)
    messages.extend([temperature_payload, humidity_payload])

#for i in range(0, len(messages), 2):
    #We use an increment of 2 because we want to display temperature and humidity for one event_time at the same moment
    #print(messages[i])
    #print(messages[i + 1])
    #time.sleep(1)


## We're creating a client to publish to the Mosquitto broker
HOST = "127.0.0.1" #local IP
PORT = 1883 #usual port without encryption
QOS = 1 #I am seeting the Quality of Service to 1 in order to receive an acknowledgment from the broker for each publication. 
        #Any potential duplicates are handled by stable identifiers and duplicate-free storage. 
        # QoS set to 0 would not provide this confirmation; 
        # QoS set to 2 would add extra message exchanges without addressing any additional need identified rn.
   

client_sensor = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    protocol=mqtt.MQTTv311,
)

try:
    client_sensor.connect(HOST, PORT, keepalive=60)
    client_sensor.loop_start()

    limit = time.monotonic() + 5
    #We wait up to 5 sec for connection confirmation

    while not client_sensor.is_connected():
        if time.monotonic() >= limit:
            raise TimeoutError("Connection to Mosquitto failed.")
        time.sleep(0.05)

    print("Connection to Mosquitto succeded")

    for i in range(0, len(messages), 2):
        #We use an increment of 2 because we want to display temperature and humidity for one event_time at the same moment
    
        for payload in messages[i:i + 2]:
            info = client_sensor.publish(
                topic="sensors/kitchen",
                payload=payload,
                qos=1,
                retain=False,
            )

            if info.rc != mqtt.MQTT_ERR_SUCCESS:
                #We chose to compare with MQTT.MQTT_ERR_SUCCESS (=0) for readability reasons.
                raise RuntimeError(f"Publication Request Rejected : {info.rc}")
            
            info.wait_for_publish(timeout=5)

            if not info.is_published():
                raise TimeoutError("No confirmation from the broker.")

        time.sleep(1)

        
finally:
    client_sensor.disconnect()
    client_sensor.loop_stop()