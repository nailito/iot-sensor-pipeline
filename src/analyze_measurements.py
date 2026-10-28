import pandas as pd
from pathlib import Path
import sqlite3

project_dir = Path(__file__).resolve().parent.parent
db = project_dir / "data" / "measurements.sqlite"

con = sqlite3.connect(db)
con.row_factory = sqlite3.Row

measurements = pd.read_sql_query("""
                        SELECT * from mesures
                        ORDER BY event_time, event_id
                        """,con)
measurements["event_time"] = pd.to_datetime(measurements["event_time"])

print(measurements)