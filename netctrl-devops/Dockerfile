# Dockerfile for NetworkController DevOps
FROM python:3.9
MAINTAINER Ezra Kissel <kissel@es.net>
LABEL maintainer="kissel@es.net"

ARG NETCTRL_VERSION=0.1

RUN echo "deb http://ppa.launchpad.net/ansible/ansible/ubuntu trusty main" >> /etc/apt/sources.list
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 93C4A3FD7BB9C367
RUN apt-get update && apt-get install -y ansible vim

RUN pip3 install fabric-mgmt-cli
RUN git clone https://github.com/fabric-testbed/ManagementCli
RUN cd ManagementCli && pip3 install . && cd ..

# cleanup
RUN rm -rf ManagementCli
