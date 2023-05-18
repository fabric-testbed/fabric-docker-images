### Versions available: 0.1

Available in this repo:

- Dockerfile to generate a DevOps image for working with the FABRIC
  network controller.

### What is NetworkController DevOps

FABRIC is using Cisco NSO as its network controller and currently
relies on the Ansible nso_config module to interact with NSO over
jsonrpc.  In addition, there is a collection of YANG models and
scripts that support the instantiation of device configurations and
services.

The NetworkController DevOps image contains the toolchain and
dependencies needed to use the FABRIC data plane config scripts.

### Prerequisites

* None

### Building

```
docker build -t netctrl .
```

### How to run

#### Ansible scripts

```
git clone git@github.com:fabric-testbed/NetworkController
docker run -ti -v $(pwd)/NetworkController:/NetworkController netctrl bash
cd NetworkController/devices-config/ansible
ansible-playbook -v -i inventory/fabric-cisco-dev.py sync-from.yaml
...
```

#### ManagementCLI

At the bottom of the ManagementCli config.yml is a block for the NSO
connection details. With these parameters set, we can run the included
`fabric-mgmt-cli` tool from within the conatiner and make use of the
"net" commands.

For example, list NSO devices:

```
docker run -ti --rm -e FABRIC_MGMT_CLI_CONFIG_PATH=/etc/config.yml -v /opt/ManagementCli/config-test.yml:/etc/config.yml netctrl fabric-mgmt-cli net show devices
```
