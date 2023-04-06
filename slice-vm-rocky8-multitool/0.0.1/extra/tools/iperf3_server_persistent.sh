#!/bin/bash
processes=$1
shift

start_port=5100

killall iperf3 > /dev/null 2>&1

for i in $(seq 1 $processes); do
    echo $i;
    port=$((start_port + i))

    echo iperf3 -s -p $port $@ --logfile ${file_name}_${port}_output
    iperf3 -s -p $port $@ --logfile iperf3_${port}_output &
    pids[${i}]=$!
    echo pids[${i}]
done
