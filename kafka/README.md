# Using Docker to deploy Kafka
This document shows how to deploy **Kafka cluster** using Docker and Docker-compose. It uses **3 Zookeepers** and **3 Brokers** by default. The docker-compose file can be used to run individual service on each VM or all services on single VM. In this document, it will show how to run on a single VM for demonstration purpose. 

> Note that we are assuming that the Zookeepers are running on **internal private network (not accessible from outside)** and the Kafka Brokers are opening ports (e.g. 19094, 29094, 39094) to **public** (if it is configured) with SSL and SASL enabled.

This has been tested with **CentOS Linux release 7.8.2003 (Core)**. 

&nbsp;

# What is Kafka?
- Apache Kafka is an open-source stream-processing software platform developed by LinkedIn and donated to the Apache Software Foundation, written in Scala and Java. The project aims to provide a unified, high-throughput, low-latency platform for handling real-time data feeds.
- Official website: https://kafka.apache.org/intro

&nbsp;

# 1. Configuration

> Install Docker CE and Docker-Compose if you do not have. [Link to instructions](/README.md)

## Clone Fabric Kafka docker project

```bash
git clone https://github.com/fabric-testbed/fabric-docker-images.git
```

&nbsp;

# 2. Start Kafka Cluster with SSL/SASL

This section shows how to run 3 **Kafka Brokers** with one 3 **Zookeeper** with **SSL** and **SASL (SCRAM)** enabled.

## 2.1. Modify **.env** file based on your setup

```bash
cd kafka

vim .env

# Set ZK_*, IN_BRK_*, EX_BRK_* to your VM's IP address (e.g. 192.168.30.70)

# Change KAFKA_SASL_SECRETS_DIR path accordingly
```

## 2.2. Create CA, signed certificates, keystores, and truststores

You can create private CA, signed certificates, truststores, and keystores by running **create-cert.sh**. You can change the password for keystore and truststore by editing the **create-cert.sh** file if you want to. 

```bash
cd secrets 

./create-certs.sh

# Answer 'y' or 'yes' for all prompted questions 
```

## 2.3. Start Zookeepers and Kafka Brokers

### Set environment variables first to simplify commands. Change the given IP addresses to your host IP address.

```bash
# Change the IP addresses to your host's IP address
export ZKS=192.168.30.70:22181,192.168.30.70:32181,192.168.30.70:42181
export BRKS=192.168.30.70:19094,192.168.30.70:29094,192.168.30.70:39094
```

### Start **3 Zookeepers** and create admin account

The **admin** account is used to communicate between Kafka brokers. This account needs to be set first on the **Zookeepers** so that **Kafka Brokers** can make connections with **Zookeepers** with given user name and password.

```bash
# Start up 3 Zookeepers (detached mode)
docker-compose up -d zookeeper-sasl-1 zookeeper-sasl-2 zookeeper-sasl-3

# Check logs (check errors)
docker-compose logs -f zookeeper-sasl-1 zookeeper-sasl-2 zookeeper-sasl-3

# Check list of topics
docker-compose exec zookeeper-sasl-1 kafka-topics --zookeeper $ZKS --list

# Create admin user on Zookeeper
docker-compose exec zookeeper-sasl-1 kafka-configs --zookeeper $ZKS --alter --add-config 'SCRAM-SHA-512=[password=change0987],SCRAM-SHA-256=[password=change0987]' --entity-type users --entity-name admin
```

> If **Zookeepers** cannot communicate each other (refusing connections), then you should open ports using **firewall-cmd** (shown in section 2.6 below) and also possibly add **security group policy** in the controller in case of using **OpenStack** or **Proxmox**. 

> Note that you can change default password of admin user. However, the password of **KafkaServer** in each **broker1_jaas.conf, broker2_jaas.conf, and broker3_jaas.conf** also needs to be changed accordingly. 

### Start **3 Kafka Brokers**

```bash
# Start up 3 Kafka Brokers (detached mode)
docker-compose up -d kafka-sasl-1 kafka-sasl-2 kafka-sasl-3

# Check logs (check errors)
docker-compose logs -f kafka-sasl-1 kafka-sasl-2 kafka-sasl-3
```

### Check status of docker images

```bash
docker-compose ps
           Name                        Command            State   Ports
-----------------------------------------------------------------------
kafka-fabric_kafka-sasl-1_1   /etc/confluent/docker/run   Up
kafka-fabric_kafka-sasl-2_1   /etc/confluent/docker/run   Up
kafka-fabric_kafka-sasl-3_1   /etc/confluent/docker/run   Up
zookeeper-sasl-1              /etc/confluent/docker/run   Up
zookeeper-sasl-2              /etc/confluent/docker/run   Up
zookeeper-sasl-3              /etc/confluent/docker/run   Up
```

## 2.4. Create a topic (fabric-test-topic)

Create a test topic (**fabric-test-topic**).

```bash
# Create fabric-test-topic once the brokers are up and ready
docker-compose exec zookeeper-sasl-1 kafka-topics --zookeeper $ZKS --create --topic fabric-test-topic --replication-factor 3 --partitions 3
```

## 2.5. Create users (reader, writer) with ACL 

Create two user accounts (**reader** - for consumer, **writer** - for producer) with ACL (**Access Control Lists**).

```bash
# Create reader user
docker-compose exec zookeeper-sasl-1 kafka-configs --zookeeper $ZKS --alter --add-config 'SCRAM-SHA-512=[password=fbreader2050],SCRAM-SHA-256=[password=fbreader2050]' --entity-type users --entity-name reader

# Create writer user
docker-compose exec zookeeper-sasl-1 kafka-configs --zookeeper $ZKS --alter --add-config 'SCRAM-SHA-512=[password=fbwriter2050],SCRAM-SHA-256=[password=fbwriter2050]' --entity-type users --entity-name writer

# Give consumer access to reader user on fabric-test-topic
docker-compose exec zookeeper-sasl-1 kafka-acls --authorizer-properties zookeeper.connect=$ZKS --add --allow-principal User:reader --consumer --topic fabric-test-topic --group '*'

# Give producer access to writer user on fabric-test-topic
docker-compose exec zookeeper-sasl-1 kafka-acls --authorizer-properties zookeeper.connect=$ZKS --add --allow-principal User:writer --producer --topic fabric-test-topic
```

> You can change default password of reader or writer user. However, the password of **sasl.jaas.config** in **reader.config** and **writer.config** also need to be changed accordingly if you change the password. 

## 2.6. Produce and consume on the **fabric-test-topic** topic

You can produce and consume on the created **fabric-test-topic** from outside of containers. However, if you are accessing it from remote host in the private or public network, then you have to add firewall rules for the ports. The commands below shows **firewall-cmd** for CentOS 7.

```bash
# For Zookeepers: Allow private IP ranges for ports
sudo firewall-cmd --permanent --zone=internal --add-source=192.168.30.0/24
sudo firewall-cmd --permanent --zone=internal --add-port=22888/tcp
sudo firewall-cmd --permanent --zone=internal --add-port=32888/tcp
sudo firewall-cmd --permanent --zone=internal --add-port=42888/tcp
sudo firewall-cmd --permanent --zone=internal --add-port=23888/tcp
sudo firewall-cmd --permanent --zone=internal --add-port=33888/tcp
sudo firewall-cmd --permanent --zone=internal --add-port=43888/tcp
sudo firewall-cmd --permanent --zone=internal --add-port=22181/tcp
sudo firewall-cmd --permanent --zone=internal --add-port=32181/tcp
sudo firewall-cmd --permanent --zone=internal --add-port=42181/tcp

# For Kafka Brokers: Open ports for listeners
sudo firewall-cmd --permanent --zone=public --add-port=19092/tcp
sudo firewall-cmd --permanent --zone=public --add-port=19094/tcp
sudo firewall-cmd --permanent --zone=public --add-port=29092/tcp
sudo firewall-cmd --permanent --zone=public --add-port=29094/tcp
sudo firewall-cmd --permanent --zone=public --add-port=39092/tcp
sudo firewall-cmd --permanent --zone=public --add-port=39094/tcp

# Reload firewall rules and check 
sudo firewall-cmd --reload
sudo firewall-cmd --list-all-zones
```

You can check the ports are opened from the remote hosts by running **nc** like below.

```bash
# If the command below returns 'success', then the host that runs this command can communicate with 192.168.30.70 on port number 19092 
nc -zvw5 192.168.30.70 19092
```

> Note that you may also need to change security group policy if you are using Proxmox or OpenStack VM. 

To run console producer and consumer, it requires to download Kafka binaries from Apache Kafka. 

> Reference: [Kafka Quick Start](https://kafka.apache.org/quickstart)

```bash
wget http://apache.mirrors.hoobly.com/kafka/2.5.0/kafka_2.12-2.5.0.tgz

tar -xzf kafka_2.12-2.5.0.tgz

cd kafka_2.12-2.5.0/bin
```

Start two bash shells on a host and run publisher and consumer. 

> You also may need to install Java if it is not installed on your host. [Install Java on CentOS](https://www.digitalocean.com/community/tutorials/how-to-install-java-on-centos-and-fedora)

#### Console Producer Test

> Change path to the **keystore** and **truststore** in the **secrets/writer.config** and **secrets/reader.config** files before testing producer and consumer. 

> If you set your own passwords for creating **writer** and **reader**, then change password in the **secrets/writer.config** and **secrets/reader.config** files accordingly.

```bash
# Change the IP addresses to your host's IP address
export BRKS=192.168.30.70:19094,192.168.30.70:29094,192.168.30.70:39094

# Change path to truststore and keystore in writer.config file
~/kafka/bin/kafka-console-producer.sh --broker-list $BRKS --topic fabric-test-topic --producer.config secrets/writer.config
```

#### Console Consumer Test

```bash
# Change the IP addresses to your host's IP address
export BRKS=192.168.30.70:19094,192.168.30.70:29094,192.168.30.70:39094

# Change path to truststore and keystore in reader.config file
~/kafka/bin/kafka-console-consumer.sh --bootstrap-server $BRKS --topic fabric-test-topic --consumer.config secrets/reader.config
```

&nbsp;

# 3. Other useful commands

## 3.1 Start interactive bash shell for Zookeeper

```bash
docker-compose exec zookeeper-sasl-1 bash
```

&nbsp;

# 4. Stop Kafka & Clear Up

Stop service, remove containers, then remove volumes. 

```bash
docker-compose stop
docker-compose rm
docker-compose down -v
```

&nbsp;

# 5. Reference

- Confluent Kafka Docker Images: [https://github.com/confluentinc/cp-docker-images](https://github.com/confluentinc/cp-docker-images)
- Kafka (not official): [https://hub.docker.com/r/bitnami/kafka](https://hub.docker.com/r/bitnami/kafka)
- zookeeper: [https://hub.docker.com/_/zookeeper](https://hub.docker.com/_/zookeeper)
- Kafka authentication using SASL/SCRAM: [https://medium.com/@hussein.joe.au/kafka-authentication-using-sasl-scram-740e55da1fbc](https://medium.com/@hussein.joe.au/kafka-authentication-using-sasl-scram-740e55da1fbc)
- husseion-joe/kafka-security-ssl-sasl: [https://github.com/hussein-joe/kafka-security-ssl-sasl](https://github.com/hussein-joe/kafka-security-ssl-sasl)
- wurstmeister/kafka-docker: [https://github.com/wurstmeister/kafka-docker](https://github.com/wurstmeister/kafka-docker)
- Kafka connectivity: [https://github.com/wurstmeister/kafka-docker/wiki/Connectivity](https://github.com/wurstmeister/kafka-docker/wiki/Connectivity)

