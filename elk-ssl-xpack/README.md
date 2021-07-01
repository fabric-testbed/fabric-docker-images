# X-Pack enabled Elastic Stack with Nginx    

This Github document shows how to set up **X-Pack security enabled** ELK stack with **SSL** using Nginx as a reverse proxy. X-Pack enabled ELK stack uses SSL encryption to communicate with other components of ELK stack or clients. It also allows **Role-based user control** that you can manage in the Kibana. Nginx redirects port 80 traffic to port 443. It redirects traffic from port 443 to Kibana port, which is 5601. The Nginx requires **a public CA signed SSL certificate** to avoid privacy warnings. ELK stack sets up its own private CA internally and signs certificates for ELK stack components (Kibana, Logstash, and Elasticsearch).

This has been tested with **CentOS Linux release 7.5.1804 (Core)** and **Ubuntu 20.04 LTS**.

&nbsp;

# What is Elastic Stack (ES or ELK)?

- "ELK" is the acronym for three open source projects: Elasticsearch, Logstash, and Kibana. Elasticsearch is a search and analytics engine. Logstash is a server‑side data processing pipeline that ingests data from multiple sources simultaneously, transforms it, and then sends it to a "stash" like Elasticsearch. Kibana lets users visualize data with charts and graphs in Elasticsearch. The Elastic Stack is the next evolution of the ELK Stack.
- Official website: https://www.elastic.co/

&nbsp;

# 1. Configuration

## 1.1 Installing Docker and Docker-Composer

> Install Docker CE and Docker-Compose if you do not have. [Link to instructions](/README.md)

You may need to increase max_map_count on the Docker host.

```bash
sudo sysctl -w vm.max_map_count=262144
```

## 1.2 Git clone

```bash
git clone https://github.com/fabric-testbed/fabric-docker-images.git
```

## 1.3 Generate CSR (Certificate Signing Request)

Create CSR for the Nginx and get a signed SSL certificate from a public CA.

```bash
openssl req -new -newkey rsa:2048 -nodes -keyout your.hostname.com.key -out your.hostname.com.csr
```

> You can change `docker-compose.yml` file to adjust required RAM for each container (`es01`, `es02`, `es03`, and `logstash`) based on your host VM's available resource. By default, each container uses `4GB`. Therefore, you may need `16GB` RAM in your host VM.

&nbsp;

# 2. Create own certificates for ELK stack components

By running create-certs docker-compose file, it will automatically create all certificates signed by own private CA for components of ELK stack.

```bash
cd fabric-docker-images/elk-ssl-xpack
docker-compose -f create_certs.yml run --rm create_certs
```

&nbsp;

# 3. Elasticsearch

## 3.1 Create data folders and start 3 nodes for ES cluster

```bash
./setdatafolders.sh
docker-compose up -d es01 es02 es03
```

## 3.2 Setup password for pre-define users on ES cluster

Get into `es01` container and execute `./elasticsearch-setup-passwords` command. This will create randomly generate password for pre-defined users (`apm_system`, `kibana_system`, `kibana`, `logstash_system`, `beats_system`, `remote_monitoring_user`, and `elastic`).

```bash
docker-compose exec es01 bash
cd bin
./elasticsearch-setup-passwords auto --batch --url https://es01:9200
exit
```

> Keep the generated random passwords safe place. It is needed to set up ELK stack properly in the following steps.

&nbsp;

# 4. Kibana

## 4.1 Update docker-compose.yml

Update `ELASTICSEARCH_PASSWORD` of `environment` section of `kib01` in the `docker-compose.yml` file using the randomly generated password for `kibana_system` in the previous step.

```yaml
kib01:
  environment:
    ELASTICSEARCH_USERNAME: kibana_system
    ELASTICSEARCH_PASSWORD: randomly-generated-password
```

## 4.2 Start Kibana

```bash
# Start kibana
docker-compose up -d kib01
# Check logs
docker-compose logs -f kib01
```

&nbsp;

# 5. Nginx

## 5.1 Update Nginx configuration in docker-compose.yml file

Change a public CA signed SSL certificate and key locations under `nginx`'s `volumes` section in the `docker-compose.yml` file.

```yaml
nginx:
  volumes:
    - "/certs/your.hostname.com.cer:/etc/nginx/certs/your.hostname.com.cer"
    - "/certs/your.hostname.com.key:/etc/nginx/certs/your.hostname.com.key"
```

## 5.2 Update Nginx configuration in `nginx/etc/nginx.conf`

Change the `your.hostname.com` to your FQDN that matches your SSL certificate signed by a public CA.

```bash
server {
  listen       80 default_server;
  server_name  your.hostname.com; # Change to your FQDN
  return 301 https://$host$request_uri;
}

server {
  listen       443 ssl http2 default_server;
  listen       [::]:443 ssl http2 default_server;
  server_name  your.hostname.com; # Change to your FQDN

  access_log /var/log/nginx/nginx.vhost.access.log;
  error_log /var/log/nginx/nginx.vhost.error.log;

  ssl_certificate "/etc/nginx/certs/your.hostname.com.cer"; # Change to your cert
  ssl_certificate_key "/etc/nginx/certs/your.hostname.com.key"; # Change to your key
}
```

## 5.3 Start Nginx

```bash
docker-compose up -d nginx
docker-compose logs -f nginx
```

&nbsp;

# 6. Logstash

The Logstash requires PKCS8 format key to use SSL encryption on its pipeline. To convert it, we need to use `openssl` installed Ubuntu docker container with access to shared certificate volume.

## 6.1 Build ubuntu docker container

```bash
docker-compose build ubuntu
```

## 6.2 Run ubuntu docker container and convert key to PKCS8

```bash
docker-compose run ubuntu
# Inside ubuntu docker container
cd /usr/share/elasticsearch/config/certificates/logstash
openssl pkcs8 -in logstash.key -topk8 -nocrypt -out logstash.pkcs8.key
chmod 664 logstash.pkcs8.key
exit
```

## 6.3 Update `logstash.yml` file

Change password of `xpack.monitoring.elasticsearch.password` in the `logstash/config/logstash.yml` file. The password has been automatically generated in the previous step.

```bash
xpack.monitoring.elasticsearch.username: logstash_system
xpack.monitoring.elasticsearch.password: 'logstash_system-password-here'
```

## 6.4 Update `01.beat.conf` file

Change password of `password` in the `output` section of `logstash/pipeline/01.beat.conf` file. The password has been automatically generated in the previous step.

```bash
# Output
output {
  elasticsearch {
    hosts => ["https://es01:9200"]
    cacert => "/usr/share/elasticsearch/config/certificates/ca/ca.crt"
    index => "%{[@metadata][beat]}-%{[@metadata][version]}-%{+YYYY.MM.dd}"
    user => "elastic"
    password => "elastic-password-here"
  }
}
```

## 6.5 Start Logstash

```bash
docker-compose up -d logstash
docker-compose logs -f logstash
```

## 6.6 Copy ELK stack's own CA certificate

You will need ELK stack's own CA certificate if you send data from remote clients using Beats (e.g. Filebeat, Metricbeat). Code below shows how to copy the certificate from `es01` container's shared volume.

```bash
docker cp es01:/usr/share/elasticsearch/config/certificates/ca/ca.crt ca.crt
```

&nbsp;

# 7. Metricbeat

This section shows how to set up a Metricbeat from remote clients that use SSL encryption to send data to ELK stack.

> Copy ELK stack's own CA certificate file `ca.crt` to remote client

## 7.1 Install Metricbeat

> Metricbeat version 7.8.1 is used to match our ELK stack's version

```bash
curl -L -O https://artifacts.elastic.co/downloads/beats/metricbeat/metricbeat-7.8.1-x86_64.rpm
sudo rpm -vi metricbeat-7.8.1-x86_64.rpm
sudo systemctl enable metricbeat
```

## 7.2 Add host `logstash` in `/etc/hosts`

```bash
sudo vim /etc/hosts

# Add IP address of ELK stack and set host name as logstash
ip_address_of_elk  logstash
```

## 7.3 Update `/etc/metricbeat/metricbeat.yml`

Update the password of `beats_system` under `output.logstash` in the `/etc/metricbeat/metricbeat.yml` on the remote client.

Update the file location of `ssl.certificate_authorities` to the ELK's own CA certificate file `ca.crt`.

```yaml
# ------------------------ Logstash Output -------------------------
output.logstash:
  # The Logstash hosts
  hosts: ["logstash:5044"]
  username: "beats_system"
  password: "beats_system-password-here"

  # Optional SSL. By default is off.
  # List of root certificates for HTTPS server verifications
  ssl.certificate_authorities: ["/certs/ca.crt"]
```

## 7.4 Start Metricbeat

Start Metricbeat on the remote client.

```bash
sudo systemctl start metricbeat
```

&nbsp;

# 8. Reference

- [Elasticsearch docker hub](https://hub.docker.com/_/elasticsearch)
- [Logstash docker hub](https://hub.docker.com/_/logstash)
- [Kibana docker hub](https://hub.docker.com/_/kibana)
- [Running the Elastic Stack on Docker](https://www.elastic.co/guide/en/elastic-stack-get-started/current/get-started-docker.html)
- [Configuring SSL, TLS, and HTTPS to secure Elasticsearch, Kibana, Beats, and Logstash](https://www.elastic.co/blog/configuring-ssl-tls-and-https-to-secure-elasticsearch-kibana-beats-and-logstash)
- [Secure communication with Logstash](https://www.elastic.co/guide/en/beats/filebeat/current/configuring-ssl-logstash.html)
- [SSL client fails to connect to Logstash](https://www.elastic.co/guide/en/beats/packetbeat/current/ssl-client-fails.html)
- [elasticsearch-certutil](https://www.elastic.co/guide/en/elasticsearch/reference/current/certutil.html)
