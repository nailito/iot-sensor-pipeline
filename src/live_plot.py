import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import sqlite3
from matplotlib.animation import FuncAnimation
import matplotlib.dates as mdates

project_dir = Path(__file__).resolve().parent.parent
db = project_dir / "data" / "measurements.sqlite"

plt.style.use("dark_background")
fig, axes = plt.subplots(2, 1, figsize=(12, 7), sharex=True)

temperature_line, = axes[0].plot([], [], color="coral", linewidth=1)
axes[0].set_title("Temperature over time")
axes[0].set_ylabel("Temperature (°C)")
axes[0].grid(alpha=0.2)

humidity_line, = axes[1].plot([], [], color="deepskyblue", linewidth=1)
axes[1].set_title("Relative humidity over time")
axes[1].set_ylabel("Humidity (%)")
axes[1].set_xlabel("Date")
axes[1].grid(alpha=0.2)

fig.suptitle("Live kitchen sensor measurements", fontsize=15)

plt.tight_layout()

def update(graph):
    con = sqlite3.connect(db)
    live_data = pd.read_sql_query("""
                            SELECT * from mesures
                            ORDER BY event_time, event_id
                            """,con)
    con.close()

    live_data["event_time"] = pd.to_datetime(live_data["event_time"])
    humidity = live_data.loc[live_data['unit'] == '%', ['event_time', 'value']].reset_index(drop=True)
    temperature = live_data.loc[live_data['unit'] == '°C', ['event_time', 'value']].reset_index(drop=True)

    temperature_line.set_data(temperature["event_time"], temperature["value"])
    humidity_line.set_data(humidity["event_time"], humidity["value"])

    for ax in axes:
        ax.relim()
        ax.autoscale_view()

animation = FuncAnimation(fig, update, interval=1000, cache_frame_data=False)

axes[1].xaxis.set_major_locator(mdates.AutoDateLocator())
axes[1].xaxis.set_major_formatter(mdates.DateFormatter("%d/%m %H:%M"))

fig.autofmt_xdate()

plt.show()