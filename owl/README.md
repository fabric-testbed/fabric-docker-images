# OWL (One-way Latency)

## What is OWL?
OWL is a FABRIC Measurement Framework service module that measures the one-way 
network latency between the source and destination hosts by injecting probe UDP packets 
timestamped by the sender and recording the arrival time on the destination node. 
Collected data are saved as .pcap files. While intended for FABRIC, it should run 
on any enrivonments that meet the following. 


## Prerequisites
1. One local directory to be mounted where output (`.pcap`) data will be saved. 
2. If running `NodeSockManager.py` (see below), another local directory to be
mounted where `owl.conf` and `links.json` files must be kept
3. While not required, hosts should have PTP (Precision Time Protocol) service running
to obtain precise measurements


## Current Limitations
- IPv4 only
- Source and destination hosts  must not be routing devices


## How to Run

### Using socket operation scripts (simpler method)

#### source (sender) side

```
$sudo docker run --rm -dp <port_num>:<same_port_num> \
--network="host"  \
--pid="host" \
--privileged \
fabrictestbed/owl:<version>  sock_ops/udp_sender.py [options]


# Example
sudo docker run -dp 5005:5005 \
--network="host"  \
--pid="host" \
--privileged \
fabrictestbed/owl:<version>  sock_ops/udp_sender.py  \
--ptp-so-file "/MeasurementFramework/user_services/owl/owl/sock_ops/time_ops/ptp_time.so" \
--dest-ip "10.0.0.2" --dest-port 5005 --frequency 0.1 \
--seq-n 5452 --duration 60

```

#### destination (receiver) side

```
$sudo docker run --rm -dp <port_num>:<port_num> \
--mount type=bind,source=<path/to/local/output/dir>,target=/owl_output \
--network="host"  \
--pid="host" \
--privileged \
fabrictestbed/owl:<version>  sock_ops/udp_capturer.py [options]

# Example
$sudo docker run -dp 5005:5005 \
--mount type=bind,source=/home/username/owl/output/,target=/owl_output \
--network="host"  \
--privileged \
fabrictestbed/owl:<version> sock_ops/udp_capturer.py \
--ip "10.0.0.2" --port 5005 --pcap-sec 60 \
--outdir /owl_output --duration 60

```

### Using `NodeSockManger.py` 

Recommended when latency measurements should be taken on multiple source-destination
pairs concurrently. A host can (but does not have to) be both the source and 
destination at the same time, for example. A host can also be the source for 
multiple destinations, vice versa.

#### Additional Requirement

A local directory containing `owl.conf` and `links.json` files.  For the format
of both files, check `https://github.com/fabric-testbed/MeasurementFramework`


#### How to run

```
# All nodes
$ sudo docker run [--rm] -dp <port_num>:<same_port_num> \
--mount type=bind,source=<path/to/local/config/dir>,target=/owl_config \
--mount type=bind,source=<path/to/local/output/dir>,target=/owl_output  \
--network="host"  \
--pid="host" \
--privileged \
fabrictestbed/owl:<version>  NodeSockManager.py /owl_config/owl.conf


$ sudo docker run --rm -dp 5005:5005 \
--mount type=bind,source=~/mydir/owl/config,target=/owl_config \
--mount type=bind,source=~/mydir/owl/output,target=/owl_output  \
--network="host"  \
--pid="host" \
--privileged \
fabrictestbed/owl:<version>  NodeSockManager.py /owl_config/owl.conf
```

## Processing Output Data (`*.pcap` files)

(may still be buggy)

```
docker run --rm -dp  \
--mount type=bind,source=~/mydir/owl/output,target=/owl_output  \
--privileged \
fabrictestbed/owl:<version>  DataProcessManager.py process /owl_output out.csv
```


