import pandas as pd
from pathlib import Path
import sqlite3

project_dir = Path(__file__).resolve().parent.parent
db = project_dir / "data" / "measurements.sqlite"

con = sqlite3.connect(db)

measurements = pd.read_sql_query("""
                        SELECT * from mesures
                        ORDER BY event_time, event_id
                        """,con)

con.close()

measurements["event_time"] = pd.to_datetime(measurements["event_time"])

humidity = measurements.loc[measurements['unit'] == '%', 'value']
temperature = measurements.loc[measurements['unit'] == '°C', 'value']

print(f"Number of rows : {measurements.shape[0]}")
print(f"Period Covered {measurements['event_time'].min()} to {measurements['event_time'].max()}")
print(f"Humidity min : {round(humidity.min(),1)} % | Humidity max : {round(humidity.max(),1)} % | Humidity mean : {round(humidity.mean(),1)} %")
print(f"Temperature min : {temperature.min()} °C | Temperature max : {temperature.max()} °C | Temperature mean : {round(temperature.mean(),1)} °C")