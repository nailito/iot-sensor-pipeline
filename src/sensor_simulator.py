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
    for col in df.columns:
        message[col] = raw_data[col]
    payload = json.dumps(message, ensure_ascii=False) #ascii=False because we have ° for the temp
    messages.append(payload)

print(messages)