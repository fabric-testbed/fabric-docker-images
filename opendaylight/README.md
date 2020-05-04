### Versions available:

Available in this repo:
- magnesium (0.12), latest: ([Dockerfile](magnesium/))

### What is OpenDaylight (ODL)

- OpenDaylight is a modular SDN controller platform.  This containerized
version of ODL includes BGP-LS and PCEP features used by the SENSE
orchestrator.

### TODO

- Configure persistent storage file
- Finalize feature list for FABRIC/SENSE

### How to run

```
docker run -ti -d --name odl -p 8181:8181 -p 8101:8101 fabrictestbed/opendaylight
```

