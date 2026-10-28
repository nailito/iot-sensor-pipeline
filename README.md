# iot-sensor-pipeline

I am building a system that simulates a temperature and humidity sensor, transmits its readings via MQTT, stores them, and visualizes their trends over time.

The goal is to explore the processing of simulated sensor data as it arrives and to evaluate the system's behavior when it receives invalid messages, duplicates, or conflicting measurements..

## Architecture

-> Python Simulator
The [simulator](src/sensor_simulator.py) represents a sensor that sends temperature and humidity readings as JSON messages.
Since I don't (yet) have such sensors, I'm simulating this data using historical readings [Appliances Energy Prediction dataset](https://doi.org/10.24432/C5VC8G).
The simulator publishes these messages to the `sensors/kitchen` topic on the
Mosquitto MQTT broker.

-> Broker MQQT Mosquitto
The broker receives the messages published by the simulator and forwards them
to clients subscribed to the `sensors/kitchen` topic.

-> Python receiver
The [receiver](src/sensor_receiver.py) subscribes to the `sensors/kitchen`
topic and validates each message before storing it in the SQLite database.

It rejects invalid messages and identifies duplicates or conflicts using
each measurement's event ID. It also displays a running summary of the
messages received.

-> SQLite database

The database stores valid measurements, including their original measurement
time and the time at which they were received.

-> Live visualization (live_plot.py)
The [live visualization](src/live_plot.py) reads the database regularly
and displays the evolution of temperature and humidity over time.

## Data source

The project uses the **Appliances Energy Prediction** dataset from the
UCI Machine Learning Repository. The dataset contains historical measurements
from a house, including kitchen temperature and relative humidity aggregated
at 10-minute intervals.

Source: Candanedo, L. (2017), Appliances Energy Prediction,
<https://doi.org/10.24432/C5VC8G>

## Technologies

- Python
- MQTT and Mosquitto
- SQLite
- Pandas
- Matplotlib
- Docker Compose

## How to run

Create a virtual environment and install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Start the MQTT broker:

```bash
docker compose up -d
```

In separate terminals, activate the virtual environment and run:

```bash
python src/sensor_receiver.py
```

Wait for the subscription confirmation, then start the live chart:

```bash
python src/live_plot.py
```

Finally, start the simulator:

```bash
python src/sensor_simulator.py
```

To stop the simulation and receiver, use `Ctrl+C` in their terminals. Close the
chart window and stop the broker with:

```bash
docker compose down
```

## Validation and tests

The receiver checks the structure and contents of incoming messages.
Manual tests cover:

- Invalid humidity values and malformed JSON
- Duplicate measurements
- Conflicting measurements with the same event ID

## Limitations

This is a local educational project based on historical residential data.
The visualization displays historical measurement times as the data is replayed.