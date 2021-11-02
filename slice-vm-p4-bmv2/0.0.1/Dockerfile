FROM ubuntu:20.04

RUN apt-get update
RUN apt-get install -y cmake 
RUN apt-get install -y g++ 
RUN apt-get install -y git 
RUN apt-get install -y automake 
RUN apt-get install -y libtool 
RUN apt-get install -y libgc-dev 
RUN apt-get install -y bison 
RUN apt-get install -y flex 
RUN apt-get install -y libfl-dev 
RUN apt-get install -y libgmp-dev 
RUN apt-get install -y libboost-dev 
RUN apt-get install -y libboost-iostreams-dev 
RUN apt-get install -y libboost-graph-dev 
RUN apt-get install -y llvm  
RUN apt-get install -y pkg-config 
RUN apt-get install -y python 
RUN apt-get install -y python3-scapy 
RUN apt-get install -y python3-ipaddr 
RUN apt-get install -y python-ply 
RUN apt-get install -y tcpdump 
RUN apt-get install -y doxygen 
RUN apt-get install -y graphviz 
RUN apt-get install -y texlive-full 
RUN apt-get install -y curl 
RUN apt-get install -y vim 
RUN apt-get install -y libssl-dev 
RUN apt-get install -y lsb-core 
RUN apt-get install -y sudo 

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
RUN ./install_deps.sh
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

RUN apt-get install -y iproute2
WORKDIR /root
