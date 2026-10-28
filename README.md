# iot-sensor-pipeline

I am building a system that simulates temperature and humidity sensors, transmits their readings via MQTT, stores them, and visualizes their trends over time.

The goal here is to test real-time data processing from sensors and to evaluate the system's behavior in the event of invalid messages, duplicates, or conflicts.

## Architecture

-> Python Simulator (sensor_simulator.py).
Its purpose is to simulate two sensors that would send temperature and humidity readings as JSON messages. Since I don't (yet) have any such sensors on hand, I simulate this data by reading historical readings (Source). 
These JSON messages are then sent to the Mosquitto MQTT broker on the sensor/kitchen channel

-> Broker MQQT Mosquitto

-> Python receiver (sensor_receiver.py).
The receiver is subscribed to the “sensor/kitchen” channel on the Mosquitto MQTT broker. It then validates each message before storing it on our database (link), or returns an error in the event of an invalid message, duplicates, or conflicts. It sends a real-time report on the messages received.

-> SQLite database

-> Live visualization (live_plot.py)
The live visualization reads the database regularly and displays how
temperature and humidity change over time.

## Data source

## Technologies

## How to run

## Validation and tests

## Limitations