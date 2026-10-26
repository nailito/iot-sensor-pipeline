import pandas as pd
from pathlib import Path

file = Path("data") / "energydata_complete.csv"

df = pd.read_csv(file)
print(df.head())