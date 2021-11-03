# Dockerfile for experimenter vms needing network tools (iperf3, etc.)
FROM ubuntu:20.04
MAINTAINER Paul Ruth <pruth@renci.org>
LABEL maintainer="pruth@renci.org"

ARG SLICE_VM_UBUNTU20_NETWORK_TOOLS_VERSION=0.0.1


RUN apt-get update
RUN apt-get install -y net-tools
RUN apt-get install -y iperf3


# cleanup
RUN apt-get clean all 
