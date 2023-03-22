FROM python:3.9-slim-buster
RUN apt-get update && \
    apt-get install -y tcpdump git && \
    apt-get -y install procps && \
    apt-get -y install gcc mono-mcs && \
    apt-get -y install sudo nano && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y tshark && \
    rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN git clone --branch timestamp-docker  https://github.com/fabric-testbed/MeasurementFramework.git
RUN mkdir /root/services
RUN mkdir /root/services/timestamp
RUN mkdir /root/services/timestamp/config_file
RUN mv /MeasurementFramework/user_services/timestamp/timestamp/config_file/timestamp.conf /root/services/timestamp/config_file/timestamp.conf
RUN mkdir /root/services/timestamp/elastic_index_files
RUN mv /MeasurementFramework/user_services/timestamp/timestamp/elastic_index_files/* /root/services/timestamp/elastic_index_files
RUN mkdir /root/services/timestamp/pcap_file
RUN mkdir /root/services/timestamp/service_files
RUN mv /MeasurementFramework/user_services/timestamp/timestamp/service_files/* /root/services/timestamp/service_files
RUN gcc -fPIC -shared -o /root/services/timestamp/service_files/get_ptp_time.so /root/services/timestamp/service_files/get_ptp_time.c
RUN pip install 'influxdb-client[ciso]'
RUN pip install 'pandas'

WORKDIR /root/services/timestamp/service_files

ENTRYPOINT [ "python3" ]