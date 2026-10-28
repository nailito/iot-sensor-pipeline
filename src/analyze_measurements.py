import pandas as pd
from pathlib import Path
import sqlite3
import matplotlib.pyplot as plt

plt.style.use("dark_background")
project_dir = Path(__file__).resolve().parent.parent
db = project_dir / "data" / "measurements.sqlite"

con = sqlite3.connect(db)

measurements = pd.read_sql_query("""
                        SELECT * from mesures
                        ORDER BY event_time, event_id
                        """,con)

con.close()

measurements["event_time"] = pd.to_datetime(measurements["event_time"])

humidity = measurements.loc[measurements['unit'] == '%', ['event_time', 'value']].reset_index(drop=True)
temperature = measurements.loc[measurements['unit'] == '°C', ['event_time', 'value']].reset_index(drop=True)

h_min, h_max = humidity.loc[humidity['value'].idxmin()], humidity.loc[humidity['value'].idxmax()]
t_min, t_max = temperature.loc[temperature['value'].idxmin()], temperature.loc[temperature['value'].idxmax()]

print(f"Number of rows : {measurements.shape[0]}")
print(f"Period Covered {measurements['event_time'].min()} to {measurements['event_time'].max()}")
print(f"Humidity min : {h_min['value']} (at {h_min['event_time']}) | Humidity max : {h_max['value']} (at {h_max['event_time']}) | Humidity mean : {humidity['value'].mean()}")
print(f"Temperature min : {t_min['value']} (at {t_min['event_time']}) | Temperature max : {t_max['value']} (at {t_max['event_time']}) | Temperature mean : {temperature['value'].mean()}")


fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
axes[0].plot(temperature['event_time'], temperature['value'])
axes[0].set_ylabel("Temperature (°C)")
axes[1].plot(humidity['event_time'], humidity['value'])
axes[1].set_ylabel("Humidity (%)")

plt.tight_layout()   
plt.show()