# Dockerfile for experimenter vms needing tools (iperf3, etc.)
FROM rockylinux:9
MAINTAINER Ganesh C Sankaran <sankarang@renci.org>
LABEL maintainer="sankarang@renci.org"

ARG FABRIC_MULTITOOL_ROCKYLINUX8_VERSION=0.1.0


RUN echo "umask 0000" >> /etc/bashrc


RUN  dnf install -y epel-release \
     && /usr/bin/crb enable \
     && dnf clean all \
     && rm -rf /var/cache/yum

# Basic tools -- TODO check latest python version
RUN dnf install -y python3-devel vim pciutils sudo \
        && dnf groupinstall -y "Development Tools" \
        && dnf clean all \
        && rm -rf /var/cache/yum

        # Networking tools
RUN dnf install -y centos-release-openstack-zed \
        && dnf clean all \
        && rm -rf /var/cache/yum

RUN sudo dnf config-manager --enable centos-openstack-zed

# TODO check more tools - dpdk, Jupyter - NIC NUMA
RUN dnf install -y frr \
                   httpd \
                   dhcp-client \
                   dhcp-server \
                   iproute \
                   iproute-tc \
                   net-tools \
                   tcpdump \
                   iftop \
                   openvswitch \
                   libibverbs \
                   iproute-tc \
  	&& dnf clean all \
  	&& rm -rf /var/cache/yum

# TODO check python version
RUN python3.9 -m pip install --no-cache-dir scapy rpyc ovs
RUN systemctl enable openvswitch

# Storage tools
RUN dnf install -y parted e2fsprogs \
        && dnf clean all \
        && rm -rf /var/cache/yum


# Other Tools
RUN dnf install -y sudo \
        && dnf clean all \
        && rm -rf /var/cache/yum

# cleanup
RUN dnf clean all && rm -rf /var/cache/yum

# FIX to run ping as user
RUN setcap cap_net_raw+ep /bin/ping

RUN useradd -ms /bin/bash fabric
RUN echo 'fabric ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER root
COPY extra/ /home/fabric/

# TODO check latest iperf version
WORKDIR /home/fabric
RUN curl -L https://github.com/esnet/iperf/releases/download/3.18/iperf-3.18.tar.gz > iperf-3.18.tar.gz
RUN tar -zxvf iperf-3.18.tar.gz
WORKDIR /home/fabric/iperf-3.18
RUN dnf groupinstall -y  "Development Tools"  \
        && dnf clean all \
        && rm -rf /var/cache/yum
RUN ./configure; make; make install


# TODO - NUMA settings for traffic generation (OR) separate repository ?

WORKDIR /home/fabric
RUN chown -R fabric:fabric /home/fabric/*
RUN chmod +x /home/fabric/tools/*.sh



USER fabric
WORKDIR /home/fabric


