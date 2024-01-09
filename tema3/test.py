import paho.mqtt.client as mqtt
import json
from random import choice

BATS = [99, 18, 117]
HUMIDS = [1000, 5000, 7000]
TMPS = [25.3, 27.5, 23.1]
ALARMS = [700, 1300, 2000]
AQIS = [12, 20, 32]
RSSIS = [1500, 2023, 2051]
NUM_TOPICS = 100

def main():
    client = mqtt.Client()
    client.connect("localhost")
    client.loop_start()


    for _ in range(NUM_TOPICS):
        payload1 = {
            "BAT" : choice(BATS),
            "HUMID" : choice(HUMIDS),
            "PRJ" : "SPRC",
            "TMP" : choice(TMPS),
            "status" : "OK",
            "timestamp" : "2019−11−26T03 :54:20+03:00"
        }

        client.publish('UPB/RPi_1', json.dumps(payload1))

        payload2 = {
            "Alarm": choice(ALARMS),
            "AQI": choice(AQIS),
            "RSSI": choice(RSSIS)
        }

        client.publish('UPB/ZEUS', json.dumps(payload2))
        client.publish('UPB/ZEUS', json.dumps(payload1))

    client.disconnect()
    client.loop_stop()

if __name__ == '__main__':
    main()