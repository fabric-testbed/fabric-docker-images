# OWL (One-way Latency)

## What is OWL?
OWL is a FABRIC Measurement Framework service module that measures the one-way 
network latency between the source and destination hosts by injecting probe UDP packets 
timestamped by the sender and recording the arrival time on the destination node. 
Collected data are saved as .pcap files. While intended for FABRIC, it should run 
on any enrivonments that meet the following. 


## Prerequisites
1. One local directory to be mounted where output (`.pcap`) data will be saved. 
mounted where `owl.conf` and `links.json` files must be kept
2. While not required, hosts should have PTP (Precision Time Protocol) service running
to obtain precise measurements


## Current Limitations
- IPv4 only
- Source and destination hosts  must not be routing devices


## How to Run

### Using socket operation scripts (simpler method)

#### source (sender) side

```
$sudo docker run --rm -d \
[--rm] \
--network="host"  \
--pid="host" \
--privileged \
[--name <container-name>] \
fabrictestbed/owl:<version>  sock_ops/owl_sender.py [options] 


# Example
sudo docker run -d \
--network="host"  \
--pid="host" \
--privileged \
--name owl-sender \
fabrictestbed/owl:<version>  sock_ops/owl_sender.py  \
--ptp-so-file "/owl/owl/sock_ops/ptp_time.so" \
--dest-ip "10.0.0.2" --dest-port 5005 --frequency 10 \
--seq-n 5452 \
[--duration 600]

```

#### destination (receiver) side

```
$sudo docker run -d \
[--rm] \
--mount type=bind,source=<path/to/local/output/dir>,target=/owl_output \
--network="host"  \
--pid="host" \
--privileged \
fabrictestbed/owl:<version>  sock_ops/owl_capturer.py [options]

# Example
sudo docker run -d \
--mount type=bind,source=/home/username/owl/output/,target=/owl_output \
--network="host"  \
--privileged \
--name owl-receiver \
fabrictestbed/owl:<version> sock_ops/owl_capturer.py \
--ip "10.0.0.2" \
--port 5005 \
--outdir /owl_output --duration 60

```

## Processing Output Data (`*.pcap` files)

(may still be buggy)

```
docker run --rm -d  \
--mount type=bind,source=~/mydir/owl/output,target=/owl_output  \
--privileged \
fabrictestbed/owl:<version>  data_ops/pcap_to_csv.py [--options]
```

## Send Output Data to a Running InfluxDB instance

```
sudo docker run -d \
[--rm] \
--mount type=bind,source=<path/to/local/output/dir>,target=/owl_output \
--network="host"  \
--pid="host" \
--privileged \
[--name <container-name>] \
fabrictestbed/owl:<version> data_ops/send_data.py \
--pcapfile <pcapfile> \
--token <influxdb_token> \
--org <influxdb_org> \
--url <influxdb_url> \
--desttype <desttype> \
--bucket <influxdb_bucket>

 
