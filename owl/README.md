# OWL (One-way Latency)

## Versions Available
- 0.1.0 

## What is OWL?
OWL is a FABRIC Measurement Framework service software that measures the network latency between the source and destination hosts by injecting probe UDP packets timestamped by the sender and recording the arrival time on the destination node. Collected data are saved as .pcap files.

## Limitations
Currently limited to IPv4 only

## Prerequisites
1. There must be a docker volume (recommended: `owl-output`) that holds output (`.pcap`) data. 
2. There must be a directory (recommended: `/home/mfuser/services/owl/settings`) containing `owl.conf` and `owl_service_request.json`
3. Port 5005 must be available



## How to Run

1. To collect data

```
docker run --rm -dp 5005:5005 \
--volume owl-output:/owl_data \
--volume "/home/mfuser/services/owl/settings:/owl_config"
--network="host" \
--privileged \
fabrictestbed/owl  NodeSockManager.py /owl_config/owl.conf
```

2. To extract data from pcap files and append to a csv file on a docker volume (`owl-output`)

```
docker run --rm -dp  \
--volume owl-output:/owl_data \
--volume "/home/mfuser/services/owl/settings:/owl_config"
--network="host" \
--privileged \
fabrictestbed/owl  DataProcessManager.py process /owl_data out.csv
```

3. To delete pcap files on a docker volume (`owl-output`)

```
docker run --rm -dp  \
--volume owl-output:/owl_data \
--volume "/home/mfuser/services/owl/settings:/owl_config"
--network="host" \
--privileged \
fabrictestbed/owl  DataProcessManager.py delete_pcap /owl_data
```

4. To delete csv files on a docker volume (`owl-output`)

```
docker run --rm -dp  \
--volume owl-output:/owl_data \
--volume "/home/mfuser/services/owl/settings:/owl_config"
--network="host" \
--privileged \
fabrictestbed/owl  DataProcessManager.py delete_csv /owl_data
```

