import paho.mqtt.client as mqtt
import time
import re
# import influxdb_client
# from influxdb_client.client.write_api import SYNCHRONOUS

connected_flag = False
message_flag = True


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    global connected_flag
    print("Connected with result code " + str(rc))

    # Adapter should recevive messages from all stations
    client.subscribe("#")
    connected_flag = True



# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global message_flag

    # The topic should respect the format: <location>/<station>
    pattern = r'^[a-zA-Z0-9_]+/[a-zA-Z0-9_]+$'
    if re.match(pattern, msg.topic) == False:
        return
    
    print("Received message: " + msg.topic + " -> " + msg.payload.decode())
    message_flag = True



if __name__ == "__main__":
    # set callbacks
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("mqtt.eclipseprojects.io", 1883, 60)
    client.loop_forever()
