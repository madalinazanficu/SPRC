#### SPRC Homework3 - Zanficu Madalina-Valentina 343C1
Keywords: Docker Swarm, microservices, MQTT, InfluxDB, Grafana

1. Structure: 
This assignment consists of 4 microservices defined in stack.yml.

a. **The MQTT Broker** uses the official image provided by Eclipse Mosquitto. 
Its primary role is to ensure smooth communication between multiple clients, 
specifically IoT devices functioning as data publishers, and the adapter, which acts as a subscriber.

b. **InfluxDB** utilizes the official InfluxDB 1.x version image. 
I opted for this version because it doesn't require database authentication. 
Additionally, for data persistence, I've defined a database volume.

c. For the **adapter**, I've created my own image built from a Dockerfile. 
This component connects to the broker, subscribes to all topics (#), filters messages, 
and inserts time series data into InfluxDB. 

Data flow: IoT Devices -> Broker -> Adapter -> InfluxDB.

d. **Grafana** is responsible for monitoring data from InfluxDB. 
To ensure data persistence, I've defined 'grafana-vol'. Moreover, datasources and dashboards are uploaded at startup. 
I utilized YAML files from https://grafana.com/docs/grafana/latest/administration/provisioning/ for this configuration.

For communication between containers, I have created 3 networks:
So, the adapter communicates only with the database(via **influxdb-adapter**) and MQTT broker(via **broker-adapter** network)
And grafana communicates with database only via **influxdb-grafana** network.

2. InfluxDB Schema:
This video helped me understand how time series work: https://www.youtube.com/watch?v=J4syKnsqQmg

Each entry represents a measurement <location>.<station>.<metric> at a specific timestamp, 
and includes two tags - 'location' and 'station' - to facilitate easier querying in Grafana.

3. Testing:
Run: ./run.sh
Optionally, check: docker stack ls
Access via browser: http://localhost:80
Stop: docker stack rm sprc3

4. Challenges:
- I spent a significant amount of time navigating the Grafana GUI until discovering transformations. 
I utilized features like 'Join by field', 'Rename fields by regex', 'Group by', and 'Value mapping' options 
to meet the homework requirements.

- To aid testing, having a software solution to mimic IoT devices would have been beneficial.

5. Resources:
Lab SPRC
https://grafana.com/docs/grafana/latest/panels-visualizations/configure-value-mappings/#map-a-regular-expression 
https://grafana.com/docs/grafana/latest/administration/provisioning/
https://www.influxdata.com/blog/getting-started-python-influxdb/
https://www.youtube.com/watch?v=3-7gZS4ePak&t=2217s


