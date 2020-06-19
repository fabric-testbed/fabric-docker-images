### Jupyter Docker Image

This is a custom Jupyter Notebook server Docker image containing with FABRIC Client tools installed.

The base image of this: [minimal-notebook](https://github.com/jupyter/docker-stacks/tree/master/minimal-notebook)

Reference for custom image: [link](https://github.com/jupyterhub/jupyterhub-deploy-docker/tree/master/examples/custom-notebook-server)


### How to use

Used by JupyerHub when spawning single user notebook servers in containers.

#### When using dockerSpawner:

in jupyterhub_config.py

```
c.DockerSpawner.image = fabrictestbed/jupyter-notebook:<version>
```

#### When using JupyterHub with K8S:

in config.yaml

```
singleuser:
  image:
    name: fabrictestbed/jupyter-notebook
    tag: <version>
```
