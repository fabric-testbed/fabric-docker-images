FROM docker.io/library/centos:8 AS builder

LABEL maintainer="Jennings Liu <jenningsloy318@gmail.com>"

ARG ARCH=amd64
ARG GO_VERSION=1.15.2

ENV GOROOT /usr/local/go
ENV GOPATH /go
ENV PATH "$GOROOT/bin:$GOPATH/bin:$PATH"
ENV GO_VERSION 1.15.2
ENV GO111MODULE=on 

RUN sed -i -e "s|mirrorlist=|#mirrorlist=|g" /etc/yum.repos.d/CentOS-*
RUN sed -i -e "s|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g" /etc/yum.repos.d/CentOS-*

# Build dependencies

RUN yum update -y && \
    yum install -y  rpm-build make  git && \
    curl -SL https://dl.google.com/go/go${GO_VERSION}.linux-${ARCH}.tar.gz | tar -xzC /usr/local 
RUN mkdir -p /go/src/github.com/ && \
    git clone https://github.com/jenningsloy318/redfish_exporter /go/src/github.com/jenningsloy318/redfish_exporter && \
    cd /go/src/github.com/jenningsloy318/redfish_exporter && \
    make build

FROM docker.io/library/centos:8 

COPY --from=builder /go/src/github.com/jenningsloy318/redfish_exporter/build/redfish_exporter /usr/local/bin/redfish_exporter
RUN mkdir /etc/prometheus
COPY config.yml.example /etc/prometheus/redfish_exporter.yml
CMD ["/usr/local/bin/redfish_exporter","--config.file","/etc/prometheus/redfish_exporter.yml"]


