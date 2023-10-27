# Dockerfile for experimenter vms needing RDMA and networking tools.
FROM rockylinux:9

MAINTAINER Ezra Kissel <kissel@es.net>
LABEL maintainer="kissel@es.net"

ARG FABRIC_MULTITOOL_RDMA_ROCKYLINUX9_VERSION=0.0.1

ENV IPERF3_RELEASE iperf-3.15-mt-beta1
ENV MOFED_VER 23.07-0.5.1.2
ENV OS_VER rhel9.2
ENV PLATFORM x86_64
ENV MOFED_DIR MLNX_OFED_LINUX-${MOFED_VER}-${OS_VER}-${PLATFORM}

RUN  dnf install -y epel-release \
     && /usr/bin/crb enable

# Basic tools 
RUN dnf install -y python3 python3-devel vim pciutils sudo \
        && dnf groupinstall -y "Development Tools"

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
                   libibverbs \
                   iproute-tc \
		   parted \
		   e2fsprogs \
		   sudo \
		   perl-sigtrap \
		   ethtool \
		   tcl \
		   lsof \
		   numactl-libs \
		   gcc-gfortran \
		   tk

USER root
WORKDIR /home/fabric

RUN curl -L https://github.com/esnet/iperf/archive/refs/tags/${IPERF3_RELEASE}.tar.gz -o ${IPERF3_RELEASE}.tar.gz
RUN tar -zxvf ${IPERF3_RELEASE}.tar.gz
RUN cd iperf-${IPERF3_RELEASE} && \
    ./configure && make && make install && \
    cd .. && \
    rm -rf iperf*

RUN curl -L http://content.mellanox.com/ofed/MLNX_OFED-${MOFED_VER}/MLNX_OFED_LINUX-${MOFED_VER}-${OS_VER}-${PLATFORM}.tgz \
      -o MLNX_OFED_LINUX-${MOFED_VER}-${OS_VER}-${PLATFORM}.tgz
RUN tar -xvf MLNX_OFED_LINUX-${MOFED_VER}-${OS_VER}-${PLATFORM}.tgz
RUN ${MOFED_DIR}/mlnxofedinstall --user-space-only --without-fw-update -q && \
    rm -rf ${MOFED_DIR} *.tgz

# Install xfer_test TCP/RDMA benchmark
RUN git clone http://github.com/disprosium8/xfer_test && \
    cd xfer_test && make rdma && \
    cp xfer_test /usr/local/bin && \
    cd .. && \
    rm -rf xfer_test

# Cleanup
RUN dnf clean all && rm -rf /var/cache/yum

RUN pip install --upgrade pip
RUN pip install --no-cache-dir scapy rpyc

RUN echo "umask 0000" >> /etc/bashrc

COPY extra/ /home/fabric/

# FIX to run ping as user
RUN setcap cap_net_raw+ep /bin/ping

RUN useradd -ms /bin/bash fabric
RUN echo 'fabric ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN chown -R fabric:fabric /home/fabric/*
RUN chmod +x /home/fabric/tools/*.sh

USER fabric
WORKDIR /home/fabric
