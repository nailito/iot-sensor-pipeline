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

## Technologies

## How to run

## Validation and tests

## Limitations