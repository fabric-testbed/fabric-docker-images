# Dockerfile for NetworkController DevOps
FROM python:3.8
MAINTAINER Ezra Kissel <kissel@es.net>
LABEL maintainer="kissel@es.net"

ARG NETCTRL_VERSION=0.1

ENV MODFILE=cisco-iosxr_models.tar.gz

RUN echo "deb http://ppa.launchpad.net/ansible/ansible/ubuntu trusty main" >> /etc/apt/sources.list
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 93C4A3FD7BB9C367
RUN apt-get update && apt-get install -y ansible vim

RUN curl https://downloads.es.net/public/kissel/models/$MODFILE -o $MODFILE
RUN tar -xf $MODFILE
RUN pip3 install ./models
RUN pip3 install requests pyangbind

# cleanup
RUN rm $MODFILE
