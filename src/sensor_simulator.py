import pandas as pd
from pathlib import Path
import json

project_dir = Path(__file__).resolve().parent.parent
file = project_dir / "data" / "energydata_complete.csv"

df_raw = pd.read_csv(file)

df = df_raw[["date", "T1", "RH_1"]].copy()
df = df.sort_values("date")

messages = []

for index, raw_data in df.head(5).iterrows():
    message = {}
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

