import pandas as pd
from pathlib import Path

file = Path("data") / "energydata_complete.csv"

df_raw = pd.read_csv(file)

df = df_raw[["date","T1","RH_1"]]
df["date"] = pd.to_datetime(df['date'])
df = df.sort_values("date")
df = df.set_index("date")

print(df)