### JupyterHub for Kubernetes

This is a custom [jupyterhub/k8s-hub](https://hub.docker.com/r/jupyterhub/k8s-hub) image, it uses [fabricauthenticator](https://github.com/fabric-testbed/fabricauthenticator) for user authentication and authorization.

Official GitHub: [https://github.com/jupyterhub/zero-to-jupyterhub-k8s](https://github.com/jupyterhub/zero-to-jupyterhub-k8s)

Official documentation of Jupyterhub with K8S:  [https://github.com/jupyterhub/zero-to-jupyterhub-k8s](https://github.com/jupyterhub/zero-to-jupyterhub-k8s)


### How to use

in config.yaml

```
hub:
  image:
    name: fabrictestbed/jupyterhub-k8s
    tag: <version>
```

See complete guide on Confluence for how to setup Jupyterhub on K8S