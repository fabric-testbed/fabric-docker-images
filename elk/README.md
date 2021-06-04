# Using Docker to deploy Elastic Stack (ES)

This document shows how to deploy each part (**Elasticsearch, Logstash, Kibana and Filebeat**) of **Elastic Stack (ES)** and **Nginx** using Docker and Docker-compose.

This has been tested with **CentOS Linux release 7.5.1804 (Core)** and **Ubuntu 20.04 LTS**.

&nbsp;

# What is Elastic Stack (ES or ELK)?

- "ELK" is the acronym for three open source projects: Elasticsearch, Logstash, and Kibana. Elasticsearch is a search and analytics engine. Logstash is a server‑side data processing pipeline that ingests data from multiple sources simultaneously, transforms it, and then sends it to a "stash" like Elasticsearch. Kibana lets users visualize data with charts and graphs in Elasticsearch. The Elastic Stack is the next evolution of the ELK Stack.
- Official website: https://www.elastic.co/

&nbsp;

# 1. Configuration

> Install Docker CE and Docker-Compose if you do not have. [Link to instructions](/README.md)

## 1.1 Git clone

```bash
git clone https://github.com/fabric-testbed/fabric-docker-images.git
```

## 1.2 Run bash script to set up folders

Run **./setfolder.sh** to create folders that are needed to bind with docker containers.

```bash
./setfolders.sh
```

## 1.3 Change settings for your environment

1. Change ES version if you want other version. The default is **7.11.0**. You can change it from **elk/.env** file.
2. Set IP address in the Nginx configuration. You can change **'server_name'** at **elk/nginx/etc/nginx.conf** file.

## 1.4 Increase max_map_count on Docker host

You need to increase max_map_count on the Docker host.

```bash
sudo sysctl -w vm.max_map_count=262144
```

## 1.5 Set Nginx password

### Install httpd-tools (or apache2-utils) and create password for **fabricadmin** account

> You can change **fabricadmin** to something else as you want.

**CentOS**

```bash
sudo yum install -y httpd-tools
```

**Ubuntu**

```bash
sudo apt-get install apache2-utils
```

### Set password for **fabricadmin** user

```bash
cd nginx/etc

htpasswd -c .htpasswd.user fabricadmin
```

After all configurations are set, you can run single command to bring up all containers.

```bash
docker-compose up
```

Or you can start each part (Elasticsearch, Logstash, Kibana, Nginx) separately. You can follow steps below to start each part one-by-one.

&nbsp;

# 2. Run Elasticsearch

This section shows how to build and run the **Elasticsearch** container using docker-compose.

### 1. Start Elasticsearch cluster with 3 nodes (detached mode)

```bash
docker-compose up -d es01 es02 es03
```

> Run container without **'-d'** to check if you want to check the container works.

### 2. Check if the Elasticsearch container works using CURL

> Use **docker-compose ps -a** to check status of docker containers.

```bash

$ curl http://127.0.0.1:9200/
{
  "name" : "es01",
  "cluster_name" : "es-docker-cluster",
  "cluster_uuid" : "eqbRkJy4Tt2l5HZBrah7gw",
  "version" : {
    "number" : "7.8.0",
    "build_flavor" : "default",
    "build_type" : "docker",
    "build_hash" : "757314695644ea9a1dc2fecd26d1a43856725e65",
    "build_date" : "2020-06-14T19:35:50.234439Z",
    "build_snapshot" : false,
    "lucene_version" : "8.5.1",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}
```

&nbsp;

# 3. Run Logstash

This section shows how to build and run the **Logstash** container using docker-compose.

### 1. Run Elasticsearch container

Run the Logstash to check if it works.

```bash
docker-compose up logstash
```

If everything works fine, run it as detached mode.

```bash
docker-compose up -d logstash
```

### 2. Check if Logstash container runs

```bash
docker-compose ps -a
```

&nbsp;

# 4. Run Kibana

This section shows how to build and run the **Kibana** container using docker-compose.

### 1. Run Kibana container

```bash
docker-compose up -d kibana
```

> Run container without **'-d'** to check if you want to check the container works.

### 2. Check if Logstash container runs

```bash
docker-compose ps -a
```

&nbsp;

# 5. Run Nginx

This section shows how to build and run the **Nginx** container using docker-compose. **Nginx** can be used as a reverse proxy for Kibana.

### 1. Run Nginx container

```bash
docker-compose up -d nginx
```

### 2. Check if Nginx container runs

```bash
docker-compose ps -a
```

### 3. Check if the Elastic Stack works by accessing **http://Your_IP_ADDRESS**

You can enter **'fabricadmin'** as user id and put your password you created.

&nbsp;

# 6. Setting up Filebeat on a remote host

This section shows how to install **Filebeat** and run on a remote VM or host.

> Reference: [Install Filebeat - Elastic.co](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-installation.html)

### 1. Download Filebeat using curl and install

> Try to use same version of Filebeat that you used for installing ES stack.

```bash
curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-7.6.2-x86_64.rpm

sudo rpm -vi filebeat-7.6.2-x86_64.rpm
```

### 2. Configure Filebeat

Change **/etc/filebeat/filebeat.yml** file. Set **host** under **setup.kibana** to your ES server IP address and also put your ES server IP address at **hosts** under **output.elasticsaerch**.

```yml
setup.kibana:
  host: "Your_ES_Server_IP:5601"

output.elasticsearch:
  hosts: ["Your_ES_Server_IP:9200"]
```

If you want to send data to **Logstash** instead of **Elasticsearch**, then you can enable and set **output.logstash**. Note that you have use one of them (**Logstash** or **Elasticsearch**) as output at a time. You cannot use both of them at the same time as outputs.

```yml
# Optional
output.logstash:
  hosts: ["Your_ES_Server_IP:5000"]
```

### 3. Setup and start Filebeat

```bash
sudo filebeat setup -e

sudo systemctl start filebeat

sudo systemctl enable filebeat
```

&nbsp;

# 7. Useful command references

Stop dockers & remove & tear down

```bash
docker-compose stop
docker-compose rm
docker-compose down -v
```

Display log output from services (-f follows log output)

```bash
docker-compose logs -f es01 es02 es03
```

&nbsp;

# 8. Reference

- elasticsearch docker hub: [https://hub.docker.com/\_/elasticsearch](https://hub.docker.com/_/elasticsearch)
- logstash docker hub: [https://hub.docker.com/\_/logstash](https://hub.docker.com/_/logstash)
- kibana docker hub: [https://hub.docker.com/\_/kibana](https://hub.docker.com/_/kibana)
- [Run Filebeat on Docker](https://www.elastic.co/guide/en/beats/filebeat/current/running-on-docker.html)
- [Filebeat Modules](https://www.elastic.co/guide/en/beats/filebeat/6.8/filebeat-modules.html)
