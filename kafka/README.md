# Using Docker to deploy Kafka
This document shows how to deploy **Kafka** using Docker and Docker-compose.

This has been tested with **CentOS Linux release 7.5.1804 (Core)**. 

&nbsp;

# What is Kafka?
- Apache Kafka is an open-source stream-processing software platform developed by LinkedIn and donated to the Apache Software Foundation, written in Scala and Java. The project aims to provide a unified, high-throughput, low-latency platform for handling real-time data feeds.
- Official website: https://kafka.apache.org/intro

&nbsp;

# 1. Configuration

> Install Docker CE and Docker-Compose if you do not have. [Link to instructions](/README.md)

## Clone Kafka docker project

```bash
git clone https://github.com/wurstmeister/kafka-docker.git
```

&nbsp;

# 2. Running Kafka Cluster

This section shows how to run 3 **Kafka** brokers with one **Zookeeper**.

## 1. Change KAFKA_ADVERTISE_HOST_NAME inside **docker-compose.yml** file

```bash
cd kafka-docker

vi docker-compose.yml

# Set KAFKA_ADVERTISED_HOST_NAME to your host's IP address
```

## 2. Start Kafka container

Start **Zookeeper** and start 3 **Kafka** brokers. You can change to a different number.

```bash
docker-compose up -d zookeeper

docker-compose scale kafka=3
```

Check if all containers are up and running. 

> Note the different ports bind to each Kafka broker's 9092 port.

```bash
$ docker-compose ps
Name                        Command               State                         Ports
-------------------------------------------------------------------------------------------
kafka-docker_kafka_1       start-kafka.sh                   Up      0.0.0.0:32770->9092/tcp
kafka-docker_kafka_2       start-kafka.sh                   Up      0.0.0.0:32768->9092/tcp
kafka-docker_kafka_3       start-kafka.sh                   Up      0.0.0.0:32769->9092/tcp
kafka-docker_zookeeper_1   /bin/sh -c /usr/sbin/sshd  ...   Up      0.0.0.0:2181->2181/tcp, 22/tcp, 2888/tcp, 3888/tcp
```

## 3. Create a topic

Start a Kafka shell to create a topic on the created Kafka cluster. 

```bash
./start-kafka-shell.sh YOUT_HOST_IP
```

In the Kafka shell, create a topic (**fabric**) and describe to check.

```bash
# Create a topic called fabric
$KAFKA_HOME/bin/kafka-topics.sh --create --topic fabric --partitions 3 --replication-factor 2 --bootstrap-server `broker-list.sh`

# Describe the topic you created
$KAFKA_HOME/bin/kafka-topics.sh --describe --topic fabric --bootstrap-server `broker-list.sh`
```

## 4. Publish and consume the created topic

You can publish and consume the created topic from inside and outside of containers.

### 4.1 Publish and consume from a container (inside Docker containers)

Start two Kafka shells and run publisher and consumer. Inside container, you can use **broker-list.sh** to populate brokers list automatically.

#### Producer

```bash
./start-kafka-shell.sh YOUT_HOST_IP

$KAFKA_HOME/bin/kafka-console-producer.sh --topic=fabric --broker-list=`broker-list.sh`
```

#### Consumer

```bash
./start-kafka-shell.sh YOUT_HOST_IP

$KAFKA_HOME/bin/kafka-console-consumer.sh --topic=fabric --from-beginning --bootstrap-server `broker-list.sh`
```

### 4.2 Publish and consume from host (outside Docker containers)

This requires to download Kafka binaries from Apache Kafka. 

> Reference: [Kafka Quick Start](https://kafka.apache.org/quickstart)


```bash
wget http://apache.mirrors.hoobly.com/kafka/2.5.0/kafka_2.12-2.5.0.tgz
tar -xzf kafka_2.12-2.5.0.tgz
cd kafka_2.12-2.5.0/bin
```

Start two bash shells on a host and run publisher and consumer. 

> You also may need to install Java if it is not installed on your host. [Install Java on CentOS](https://www.digitalocean.com/community/tutorials/how-to-install-java-on-centos-and-fedora)

#### Producer

```bash
# Note that the port number of localhost is mapped to one of Kafka broker
# Your port number will be different. 
# Check your mapped port by using 'docker-compose ps'
./kafka-console-producer.sh --broker-list localhost:32770 --topic fabric
```

#### Consumer

```bash
# Here, consumer used another port number from 3 brokers
./kafka-console-consumer.sh --bootstrap-server localhost:32768 --topic fabric --from-beginning
```

&nbsp;

# 3. Stop Kafka & Clear Up

Stop service, remove containers, then remove volumes. 

```bash
docker-compose stop
docker-compose rm
docker-compose down -v
```

&nbsp;

# 4. Reference

- Kafka (not official): [https://hub.docker.com/r/bitnami/kafka](https://hub.docker.com/r/bitnami/kafka)
- zookeeper: [https://hub.docker.com/_/zookeeper](https://hub.docker.com/_/zookeeper)
- wurstmeister/kafka-docker: [https://github.com/wurstmeister/kafka-docker](https://github.com/wurstmeister/kafka-docker)
- Kafka connectivity: [https://github.com/wurstmeister/kafka-docker/wiki/Connectivity](https://github.com/wurstmeister/kafka-docker/wiki/Connectivity)

