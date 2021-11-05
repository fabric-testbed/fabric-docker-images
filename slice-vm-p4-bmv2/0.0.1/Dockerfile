FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=America/New_York
RUN apt-get update && apt-get -y install \
    cmake \
    g++ \
    git \
    automake \
    libtool \
    libgc-dev \
    bison \
    flex \
    libfl-dev \
    libgmp-dev \
    libboost-dev \
    libboost-iostreams-dev \
    libboost-graph-dev \
    llvm \
    pkg-config \
    python \
    python3-scapy \
    python3-ipaddr \
    python-ply \
    tcpdump \
    doxygen \
    graphviz \
    texlive-full \
    curl \
    vim \
    libssl-dev \
    lsb-core \
    sudo \
    iproute2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /root
RUN git clone https://github.com/protocolbuffers/protobuf.git
WORKDIR /root/protobuf
RUN git checkout v3.2.0
RUN git submodule update --init --recursive
RUN ./autogen.sh
RUN ./configure
RUN make
RUN make install
RUN ldconfig

WORKDIR /root
RUN git clone --recursive https://github.com/p4lang/p4c.git
RUN mkdir /root/p4c/build
WORKDIR /root/p4c/build
RUN cmake ..
RUN make 
RUN make install

WORKDIR /root
RUN git clone https://github.com/p4lang/behavioral-model.git
WORKDIR /root/behavioral-model
RUN sed -i 's/libssl1.0-dev/libssl-dev/g' install_deps.sh 
RUN apt-get update \
    && ./install_deps.sh \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
RUN ./autogen.sh
RUN ./configure
RUN make
RUN make install
RUN ldconfig

WORKDIR /root
RUN mkdir simple_p4_router
WORKDIR /root/simple_p4_router
COPY simple_router.p4 /root/simple_p4_router
RUN p4c -b bmv2 simple_router.p4 -o simple_router.bmv2

WORKDIR /root
