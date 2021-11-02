# Dockerfile for experimenter vms needing network tools (iperf3, etc.)
FROM centos:8
MAINTAINER Paul Ruth <pruth@renci.org>
LABEL maintainer="pruth@renci.org"

ARG SLICE_VM_CENTOS8_NETWORK_TOOLS_VERSION=0.0.1


RUN yum install -y iperf3
RUN yum install -y tcpdump
 

# cleanup
RUN yum clean all 
