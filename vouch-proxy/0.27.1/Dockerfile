# voucher/vouch-proxy
# https://github.com/vouch/vouch-proxy
FROM golang:1.16 AS builder

LABEL maintainer="vouch@bnf.net"

RUN mkdir -p ${GOPATH}/src/github.com/vouch/vouch-proxy
WORKDIR ${GOPATH}/src/github.com/vouch/vouch-proxy

# Copy these files to be later picked up the scratch
RUN git clone https://github.com/fabric-testbed/vouch-proxy.git .
RUN cp -R templates /tmp
RUN cp -R static /tmp
RUN cp -R .defaults.yml /tmp

# RUN go-wrapper download  # "go get -d -v ./..."
# RUN ./do.sh build    # see `do.sh` for vouch build details
# RUN go-wrapper install # "go install -v ./..."

RUN ./do.sh goget
RUN ./do.sh gobuildstatic # see `do.sh` for vouch-proxy build details
RUN ./do.sh install

FROM scratch
LABEL maintainer="vouch@bnf.net"
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /tmp/templates /templates
COPY --from=builder /tmp/.defaults.yml /.defaults.yml
# see note for /static in main.go
COPY --from=builder /tmp/static /static
COPY --from=builder /go/bin/vouch-proxy /vouch-proxy
EXPOSE 9090
ENTRYPOINT ["/vouch-proxy"]
HEALTHCHECK --interval=1m --timeout=5s CMD [ "/vouch-proxy", "-healthcheck" ]

