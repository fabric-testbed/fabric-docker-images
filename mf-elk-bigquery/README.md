# Export Elasticsearch Data to Google Bigquery

## Purpose
The ELK data export service provided by the measurement framework is used to export the Elasticsearch data in user's fabric slice to Google Bigquery.  

## Prerequisites
To use the service, users need set up their Google Bigquery account and have an instrumentized Fabric slice. More details can be found on the Fabric learn site: 'Technical Guides' -> 'Experiment Measurement APIs(MFLib)' -> 'Export Elasticsearch Data to Google Bigquery'  

## How to Use the Service

### Download the Docker Image
```
sudo docker pull fabrictestbed/mf-elk-bigquery
```

### Run the Pulled Image as a Docker Container

```
sudo docker run -dit \
-v /PATH_TO_GOOGLE_SERVICE_ACCOUNT_KEY:/root/key.json \
--network=host \
--privileged \
--name elk-bigquery \
fabrictestbed/mf-elk-bigquery
```

### Run the Command to Dump the Data to Bigquery 

```
sudo docker exec -i elk-bigquery \
python3 elk-bigquery.py \
--query '{"query":{"range":{"@timestamp":{"gte":"now-1h"}}}}' \
--index metricbeat-7.13.2-2023.07.10-000001 \
--key key.json \
--table elk-bigquery.metricbeat.test
```

In the command above, users need to specify (1)their Elasticsearch query (2) which Elasticsearch index to query from (3) The Google service account key file that's binded to the Bigquery project and (4) the table name in the format of {project_name}.{dataset_name}.{table_name} 

