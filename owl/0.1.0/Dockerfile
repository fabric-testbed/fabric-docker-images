# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster
MAINTAINER Mami Hayashida (mami.hayashida@uky.edu)
# Currently for testing only

EXPOSE 5005

# Build dependencies
RUN apt-get update && apt-get install -y \
	tcpdump \
        git \
	&& rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install --pre scapy[basic]

# Download OWL code 
RUN git clone --branch owl  https://github.com/fabric-testbed/MeasurementFramework.git

### May be needed later
#COPY requirements.txt requirements.txt
#RUN pip3 install -r requirements.txt

RUN mkdir /owl_output
RUN mkdir /owl_config

# Confirm
RUN ls -l /

WORKDIR /MeasurementFramework/user_services/owl

# Sanity check 
RUN pwd
RUN ls -lh *

ENTRYPOINT [ "python3" ]


