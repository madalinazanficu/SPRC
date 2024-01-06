import paho.mqtt.client as mqtt
import time
import re
import json
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb import InfluxDBClient

db_client = InfluxDBClient(host="influxdb", port=8086)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Adapter should recevive messages from all stations
    client.subscribe("#")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):

    # The topic should respect the format: <location>/<station>
    pattern = r'^[^/]+/[^/]+$'
    if re.match(pattern, msg.topic) == False:
        return
    print("Received a message by topic [" + msg.topic + "]")


    # Extract entities from the topic and payload
    location = msg.topic.split("/")[0]
    station = msg.topic.split("/")[1]
    payload = json.loads(msg.payload.decode())


    # Check if payload contains timestamp or generate it
    if "timestamp" not in payload:
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    else:
        timestamp = payload["timestamp"]

    # Create a time series for each numeric entry in the payload
    for key, value in payload.items():
        if type(value) == int or type(value) == float:
            measurement = location + "." + station + "." + key
            point = influxdb_client.Point(measurement) \
                        .tag("location", location) \
                        .tag("station", station) \
                        .field("value", value) \
                        .time(timestamp)
            
            print("Writing to InfluxDB...")
            write_api = db_client.write_api(write_options=SYNCHRONOUS)
            write_api.write(bucket="weather_station", record=point)
            print("Done writing to InfluxDB")
            
            print(measurement + " -> " + str(value) + " at " + timestamp)
    


if __name__ == "__main__":

    # Create the influxdb client - using InfluxDB 1.x in order to avoid autehntication
    db_client.create_database("weather_station")
    
    # db_client.create_database("weather_station")
    print("Created InfluxDB database")

    # Create the mqtt client (which listens for messages)
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect("mqtt-broker", 1883, 60)
    mqtt_client.loop_forever()

