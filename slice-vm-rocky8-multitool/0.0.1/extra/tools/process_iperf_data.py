#!/bin/python3

import json
import time
from ipaddress import ip_address, IPv4Address, IPv6Address, IPv4Network, IPv6Network

import os
import sys

from concurrent.futures import ThreadPoolExecutor

# Define Experiment


def iperf3_process_output(summary_files=[], verbose=False):

    runs = {}
    for summary_file in summary_files:
        f = open(summary_file, "r")
        run_output = f.read()
        f.close()

        runs[summary_file] = json.loads(run_output)

    # print(f"{runs}")
    table = []
    for run_name, streams in runs.items():

        # print(f"{run_name}")

        run_bandwidth = 0.0
        run_retransmits = 0
        run_max_rtt = 0
        run_min_rtt = -1
        run_mean_rtt = 0
        run_mtu = 0

        for stream in streams:

            # for k1,v1 in stream.items():
            #    print(f"key: {k1}")

            run_mtu = stream['intervals'][0]['streams'][0]['pmtu']

            stream_port = stream['start']['connecting_to']['port']
            stream_bandwidth = stream['end']['sum_received']['bits_per_second'] * 0.000000001
            stream_retransmits = stream['end']['sum_sent']['retransmits']
            stream_max_rtt = stream['end']['streams'][0]['sender']['max_rtt'] * 0.001
            stream_min_rtt = stream['end']['streams'][0]['sender']['min_rtt'] * 0.001
            stream_mean_rtt = stream['end']['streams'][0]['sender']['mean_rtt'] * 0.001
            stream_host_total = stream['end']['cpu_utilization_percent']['host_total']
            stream_host_user = stream['end']['cpu_utilization_percent']['host_user']
            stream_host_system = stream['end']['cpu_utilization_percent']['host_system']
            stream_remote_total = stream['end']['cpu_utilization_percent']['remote_total']
            stream_remote_user = stream['end']['cpu_utilization_percent']['remote_user']
            stream_remote_system = stream['end']['cpu_utilization_percent']['remote_system']
            stream_sender_tcp_congestion = stream['end']['sender_tcp_congestion']
            stream_receiver_tcp_congestion = stream['end']['receiver_tcp_congestion']

            # print(f"Stream: {stream_port}. bw = {stream_bandwidth}")
            run_bandwidth += stream_bandwidth
            run_retransmits += stream_retransmits

            if stream_max_rtt > run_max_rtt:
                run_max_rtt = stream_max_rtt

            if stream_min_rtt < run_min_rtt or run_min_rtt == -1:
                run_min_rtt = stream_min_rtt

            run_mean_rtt += stream_mean_rtt

        run_mean_rtt = run_mean_rtt / len(streams)

        #timestamp, source, target = run_name.split('__')
        # run = len(table)

        table.append([run_name,
                      len(streams),
                      run_mtu,
                      f'{run_bandwidth:.3f}',
                      f'{run_max_rtt:.2f}',
                      f'{run_min_rtt:.2f}',
                      f'{run_mean_rtt:.2f}',
                      run_retransmits,
                      ])
        # if verbose:
        # print(f"{run_name}: pmtu: {run_mtu}, bw: {run_bandwidth:.3f} Gbps, rtt ms (max/min/mean): {run_max_rtt:.2f}/{run_min_rtt:.2f}/{run_mean_rtt:.2f} ms, retransmits: {run_retransmits}")
    #headers = ["Timestamp", "Source", "Target", "P", "pmtu", "bw", "rtt_max", "rtt_min", "rtt_mean", "retransmits"]
    #printable_table = self.create_table_local(table, title=f'iPerf3 Results', properties={'text-align': 'left'},
    #                                          headers=headers, index='Timestamp')
    #display(printable_table)

    return table


import sys, getopt

def main(argv):
    print(iperf3_process_output(argv))

if __name__ == "__main__":
   main(sys.argv[1:])
