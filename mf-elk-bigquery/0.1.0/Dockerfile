FROM python:3.9-slim-buster
RUN apt-get update && \
    apt-get -y install sudo nano && \
    pip install --upgrade pip \
    pip install elasticsearch==7.13.4 \
    pip install google-cloud-bigquery==3.11.4
RUN mkdir -p /root/elk-bigquery
COPY elk-bigquery.py /root/elk-bigquery/
WORKDIR /root/elk-bigquery
ENTRYPOINT [ "python3" ]