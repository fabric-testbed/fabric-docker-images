FROM ubuntu:latest

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
      openssl \
      openssh-client \
    && apt-get clean

