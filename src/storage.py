import pandas as pd
from pathlib import Path
import sqlite3

project_dir = Path(__file__).resolve().parent.parent
db = project_dir / "data" / "measurements.sqlite"

con = sqlite3.connect(db)
con.row_factory = sqlite3.Row


con.execute(
    """
    CREATE TABLE IF NOT EXISTS mesures (
    event_id TEXT primary key not null,
    sensor_id TEXT NOT NULL,
    event_time TEXT NOT NULL,
    value REAL NOT NULL,
    unit TEXT NOT NULL,
    received_at TEXT NOT NULL
    )
    """
            )
con.commit()

def save_measurement(data):
    try:
        cur = con.execute(
            """
            SELECT * from mesures
            where event_id = ?
            """,
            (data["event_id"],))
        
        row = cur.fetchone()
        
        if row is None: #if we dont have any row with the same event_id as the mesure we want to register
            con.execute(
                """
                INSERT INTO mesures (event_id, sensor_id, event_time, value, unit, received_at) VALUES (?,?,?,?,?,?)        
                """,
                (data["event_id"],data["sensor_id"],data["event_time"],data["value"],data["unit"],data["received_at"])
            )
            con.commit()
            return ("entered",None)
        if row["sensor_id"] != data["sensor_id"] or row["event_time"] != data["event_time"] or row["value"] != data["value"] or row["unit"] != data['unit']:
            return ("conflict",None)
        else:
            return ("duplicate",None)
        
    except sqlite3.Error:
        con.rollback()
        #if we have 
        return(None, "storage")

test_measurement = {
    "event_id": "Sensor_1:temperature:2016-01-11 17:00:00",
    "sensor_id": "Sensor_1",
    "event_time": "2016-01-11 17:00:00",
    "value": 19.89,
    "unit": "°C",
    "received_at": "2026-10-27T10:00:00+00:00",
} #for testing purpose

save_measurement(test_measurement)