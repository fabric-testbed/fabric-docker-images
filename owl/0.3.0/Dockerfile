# syntax=docker/dockerfile:1

FROM python:3.11-slim-buster
EXPOSE 5005

RUN apt-get update && \
    apt-get install -y tcpdump git build-essential && \
    apt-get install -y procps && \
    apt-get install -y gcc mono-mcs && \
    apt-get install -y sudo nano vim && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install --pre scapy[basic]
RUN pip install influxdb-client
RUN pip install --upgrade psutil
RUN pip install requests
RUN pip install influxdb3-python
RUN pip install pandas

RUN git clone  https://github.com/fabric-testbed/owl.git
RUN mkdir /owl_output
RUN mkdir /owl_config
RUN gcc -fPIC -shared -o /owl/owl/sock_ops/ptp_time.so \
	/owl/owl/sock_ops/ptp_time.c
RUN ls -l /

WORKDIR /owl/owl

### May be needed later
#COPY requirements.txt requirements.txt
#RUN pip3 install -r requirements.txt


# For debugging
RUN pwd
RUN ls -lh *

ENTRYPOINT [ "python3" ]  
