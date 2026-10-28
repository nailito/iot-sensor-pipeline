import pandas as pd
from pathlib import Path
import sqlite3

project_dir = Path(__file__).resolve().parent.parent
db = project_dir / "data" / "measurements.sqlite"



con = sqlite3.connect(db)
con.row_factory = sqlite3.Row
con.execute(
    """
    DELETE FROM mesures
    """
            )
con.commit()
con.close()
