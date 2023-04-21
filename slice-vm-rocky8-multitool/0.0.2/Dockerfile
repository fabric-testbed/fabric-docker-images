# Dockerfile for experimenter vms needing tools (iperf3, etc.)
FROM rockylinux:8
MAINTAINER Paul Ruth <pruth@renci.org>
LABEL maintainer="pruth@renci.org"

ARG FABRIC_MULTITOOL_ROCKYLINUX8_VERSION=0.0.1


RUN echo "umask 0000" >> /etc/bashrc


RUN  dnf install -y epel-release \
     && /usr/bin/crb enable \
     && dnf clean all \
     && rm -rf /var/cache/yum



# Basic tools
RUN dnf install -y  curl python3.9 python39-devel vim pciutils sudo \
        && dnf groupinstall -y "Development Tools" \
        && dnf clean all \
        && rm -rf /var/cache/yum

# Install pip
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
        && python3 get-pip.py \
        && rm -rf get-pip.py


# Networking tools
RUN dnf install -y https://repos.fedorapeople.org/repos/openstack/openstack-yoga/rdo-release-yoga-1.el8.noarch.rpm \
        && dnf clean all \
        && rm -rf /var/cache/yum


RUN dnf install -y frr \
                   httpd \
                   dhcp-client \
                   dhcp-server \
                   iproute \
                   iproute-tc \
                   net-tools \
                   tcpdump \
                   iftop \
                   iperf3 \
                   openvswitch \
                   libibverbs \
                   iproute-tc \
  	&& dnf clean all \
  	&& rm -rf /var/cache/yum

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

WORKDIR /home/fabric
RUN curl https://downloads.es.net/pub/iperf/iperf-3.13-mt1.tar.gz > iperf-3.13-mt1.tar.gz
RUN tar -zxvf iperf-3.13-mt1.tar.gz
WORKDIR /home/fabric/iperf-3.13-mt1
RUN dnf groupinstall -y  "Development Tools"  \
        && dnf clean all \
        && rm -rf /var/cache/yum
RUN ./configure; make; make install



WORKDIR /home/fabric
RUN chown -R fabric:fabric /home/fabric/*
RUN chmod +x /home/fabric/tools/*.sh



USER fabric
WORKDIR /home/fabric

