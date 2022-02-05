# Redfish Prometheus Exporter


This build creates a prometheus exporter that gathers data from redfish running on a rack's head node. The build uses the [jenningsloy318/redfish_exporter](https://github.com/jenningsloy318/redfish_exporter)

The fabric-prometheus system is containerized and run on each rack's head node. Most of the containers just use the standard builds found on DockerHub, however there is not a standard build found for this library.
This container will be installed in the fabric-prometheus system on the fabric head nodes to gather metrics available from the idrac. To run you will need to pass it a valid config file in the format of:

```
hosts:
  192.168.11.100:
	username: <redfish-username>
	password: <redfish-password>
  default:
	username: admin
	password: password
```

Where 192.168.11.100 is the location of the redfish server and 
default guards against a redfish bug if noexistent host given.
The config file needs to be mapped to the docker directory /etc/prometheus/redfish_exporter.yml


