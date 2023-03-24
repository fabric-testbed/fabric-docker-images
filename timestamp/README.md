# Timestamp Service

## Purpose
The timestamp service is a service provided by the Fabric Measurement Framework library to collect the precise timestamps for packets and events on the nodes in a Fabric slice. It also provides the option for experimenters to upload the collected timestamps to database such as InfluxDB installed on the Measurement node through the measurement network.  


## Prerequisites
To use the timestamp service, PTP (Precision Time Protocol) should be configured and running on the nodes in advance, which is implemented by the software **linuxptp**.  



## How to Collect Timestamp Data?

### Run the Pulled Image as a Docker Container

```
sudo docker run -dit \
-v /home/VolumeToMount:/root/services/timestamp/output_files/ \
--pid=host \
--network=host \
--privileged \
--name timestamp \
fabrictestbed/timestamp
```

### Collect Timestamps of Packets

```
sudo docker exec -i timestamp \
python3 /root/services/timestamp/service_files/timestamptool.py \
record packet -h
```
After running the command, experimenters can then perform their experiments to send packets.


### Read the Collected Packet Timestamps

```
sudo docker exec -i timestamp \
python3 /root/services/timestamp/service_files/timestamptool.py \
get packet -h
```

### Collect Timestamps of Events

```
sudo docker exec -i timestamp \
python3 /root/services/timestamp/service_files/timestamptool.py \
record event -h
```
The command reads the time of the PTP clock that the System clock is being synchronized to. 

### Read the Collected Event Timestamp

```
sudo docker exec -i timestamp \
python3 /root/services/timestamp/service_files/timestamptool.py \
get event -h
```

## How to Dump the Timestamp Results to Database?

The timestamp service also provides users with the option to dump the timestamp results to database, such as InfluxDB. 

### Upload the Timestamp Data 

```
sudo docker exec -i timestamp \
python3 /root/services/timestamp/service_files/influxdb_manager.py \
upload -h
```

### Download the Timestamp Data

```
sudo docker exec -i timestamp \
python3 /root/services/timestamp/service_files/influxdb_manager.py \
download -h
```
