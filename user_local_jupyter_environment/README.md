### Running FABRIC JupyterLab Containers Locally

This guide explains how to run and manage local Jupyter Notebook containers on your machine using Docker for different FABRIC releases. Each release folder contains a `docker-compose.yml` file, which allows you to launch specific containers tailored to various stages of development.

Below are the three types of containers you can run and how to access them:

#### 1. **fabric-default-\<release>**

This container runs the stable release of FABRIC's libraries (`fablib`) and hosts stable Jupyter examples. It corresponds to the default container option on FABRIC's Jupyter Hub.

To start the `fabric-default` container:
1. Navigate to the release folder (for example, version `1.7.0`).
2. Run the following command to bring up the default container:
    ```bash
    cd 1.7.0
    docker-compose up -d fabric-default
    ```

#### 2. **fabric-bleeding**

This container runs the most recent released version of `fablib` and includes the latest Jupyter examples. It corresponds to the "bleeding edge" container option on FABRIC's Jupyter Hub.

To start the `fabric-bleeding` container:
1. Navigate to the release folder (for example, version `1.7.0`).
2. Run the following command to bring up the bleeding edge container:
    ```bash
    cd 1.7.0
    docker-compose up -d fabric-bleeding
    ```

#### 3. **fabric-beyond-bleeding**

This container is the most experimental version, running `fablib` and Jupyter examples from the main branch. It includes the latest development changes and is recommended primarily for the FABRIC development team.

To start the `fabric-beyond-bleeding` container:
1. Navigate to the release folder (for example, version `1.7.0`).
2. Run the following command to bring up this development container:
    ```bash
    cd 1.7.0
    docker-compose up -d fabric-beyond-bleeding
    ```

### Accessing JupyterHub

Once the container is up and running, you can access the JupyterLab interface from your web browser by navigating to:

- **http://localhost:8888/**

**Note:** It may take up to one minute for the container to start JupyterHub.

### Accessing the Running Container

If you need to interact with the container directly, you can access its shell using the following steps:

1. **List running containers:**
   First, list the running containers to find the one you want to access:
   ```bash
   docker ps
   ```
   You should see something like this:
   ```bash
   CONTAINER ID   IMAGE                                  COMMAND               STATUS              NAMES
   abcdef123456   fabrictestbed/jupyter-notebook:3.3.8   "start-notebook.sh"   Up 2 minutes        fabric-default
   ```

2. **Access the container's shell:**
   Once you have the container name (e.g., `fabric-default`), use `docker exec` to enter the container:
   ```bash
   docker exec -it fabric-default /bin/bash
   ```
   This will drop you into the container's shell where you can run commands as if you were inside the container.

3. **Exit the container:**
   When you're done working inside the container, you can exit by typing:
   ```bash
   exit
   ```

### Important Notes:
- **Only one container can run at a time.** If you want to switch from one container to another, you must first stop and remove the existing container:
  ```bash
  docker-compose down
  ```
  Then, bring up the new container using the relevant `docker-compose up` command mentioned earlier.

- **Work Directory Mapping:** Each container maps the `~/work` directory on your local machine to the `/home/fabric/work` directory inside the container. This ensures that all work is saved locally on your machine.

- **Token Setup:** Before running any Jupyter notebooks, download an authentication token from [FABRIC's Credential Manager](https://cm.fabric-testbed.net/). Save the token in your `~/work` directory on your machine. This is required to authenticate and interact with FABRIC resources.

By following these steps, you can easily manage different FABRIC container environments, access JupyterLab via your browser, interact with the containers directly, and keep your work synced with your local machine.