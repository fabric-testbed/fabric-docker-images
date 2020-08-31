### Versions available:

This directory uses a git submodule to pull the Cisco nso-docker repository and its Docker image definitions and Makefile.

Available in this repo:
- Scripts compatible with NSO version to start the NSO docker containers.

### What is NSO

Cisco's Network Services Orchestrater.  FABRIC will be investigating the use of NSO to manage and configure its data plane switches.

### Prerequisites

* NSO installer bin from Cisco DevNet
* IOS XR NED from Cisco DevNet

### Building

```
git submodule init
git submodule update
cd nso-docker
cp <path to NSO installer bin> nso-docker/nso-install-files
make
```

This will generate `cisco-nso-dev` and `cisco-nso-base` docker images.


### How to run

Edit and execute the supplied start scripts to start with appropriate options.  For example:

```
mkdir /opt/nso-dev
mkdir /opt/nso-dev-logs
sudo ./start-dev.sh
```

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
