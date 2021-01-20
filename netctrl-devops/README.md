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
docker build -t netctrl-devops .
```

### How to run

```
git clone git@github.com:fabric-testbed/NetworkController
docker run -ti -v $(pwd)/NetworkController:/NetworkController netctrl-devops bash
cd NetworkController/devices-config/ansible
ansible-playbook -v -i inventory/fabric-cisco-dev.py sync-from.yaml
...
```
