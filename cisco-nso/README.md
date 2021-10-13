### Versions available:

This directory uses a git submodule to pull the Cisco nso-docker repository and its Docker image definitions and Makefile.

Available in this repo:
- Scripts compatible with NSO version 5.3 to start the NSO docker containers.

### What is NSO

Cisco's Network Services Orchestrater.  FABRIC will be investigating the use of NSO to manage and configure its data plane switches.

### Prerequisites

* Docker
* NSO installer bin from Cisco DevNet
* IOS XR NED from Cisco DevNet

### Preparing system (e.g. FABRIC VM)

Follow instruction for docker-ce install for Centos 8:
* https://docs.docker.com/engine/install/centos/

Install some needed dependencies:
```
sudo yum install git git-lfs make
```

### Building

Acquire NSO install and NCS IOSXR NED from NetworkController repository.

```
git clone git@github.com:fabric-testbed/NetworkController
git clone git@github.com:fabric-testbed/fabric-docker-images
cd NetworkController/nso
git lfs pull
sh nso-5.5.linux.x86_64.signed.bin
```

The last step extracts the NSO installer executable.

```
cd fabric-docker-images/cisco-nso
git submodule init
git submodule update
cp <path to NSO installer bin> nso-docker/nso-install-files
make
make NSO_VERSION=5.5 tag-release
```

This will generate `cisco-nso-dev` and `cisco-nso-base` docker images.

### Configuration

`ncs.conf` in the version subdirectory contains a custom configuration for NSO that will be mounted inside the container. This configuration works for FABRIC as currently defined in the repository but can be customized based on any specific deployment requirements.

A key aspect of the config is specifying the SSL certificate and key for the instance, see the `ssl` block. For a new NSO VM/host, a certificate will need to be provided or else a self-signed certificate will be generated and used by the NSO service.

Request a new certificate for the deployment host as described here: https://fabric-testbed.atlassian.net/wiki/spaces/FP/pages/383320076/Public+Certificates+for+FABRIC+Services

Place the resulting files (cert, key, CA chain) into `/etc/nso` and as defined in `ncs.conf`


### How to run

Edit and execute the supplied start scripts to start with appropriate options.  For example:

```
mkdir /opt/nso-dev
mkdir /opt/nso-dev-logs
sudo ./start-dev.sh
```

The `run-prod.sh` script can be used to deploy a production NSO instance.  Edit script as appropriate for deployment.

### Adding a new NED (package)

For the `dev` image, the script mount `/opt/nso` as `/nso` inside the container.  This path containers the "run state" of the NSO service.  New packages may be added under `/opt/nso/run/packages` on the host filesystem.

```
cp -r <NED DIR> /opt/nso/run/packages/
ssh admin@localhost -p 2222
admin connected from 127.0.0.1 using ssh on fabric-netest.renci.org
admin@ncs> switch cli 
admin@ncs# packages reload

>>> System upgrade is starting.
>>> Sessions in configure mode must exit to operational mode.
>>> No configuration changes can be performed until upgrade has completed.
>>> System upgrade has completed successfully.

admin@ncs> show packages 
packages package cisco-iosxr-cli-7.18
 package-version 7.18.2
 description     "NED package for the Cisco IOS XR"
 ncs-min-version [ 4.4.2 ]
 directory       /nso/run/state/packages-in-use/1/cisco-iosxr-cli-7.18
 component upgrade-ned-settings
  upgrade java-class-name com.tailf.packages.ned.iosxr.UpgradeNedSettings
 component cisco-ios-xr
  ned cli ned-id  cisco-iosxr-cli-7.18
  ned cli java-class-name com.tailf.packages.ned.iosxr.IosxrNedCli
  ned device vendor Cisco
```
