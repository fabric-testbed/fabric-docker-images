### Running FABRIC JupyterLab Containers Locally

This guide explains how to run local Jupyter Notebook containers on your machine using Docker for different FABRIC releases. Each release folder includes a `docker-compose.yml` file, which you can use to launch different containers.

Below, we describe three types of containers you can run and how to do so:

#### 1. **fabric-default-\<release>**

This container is designed to run the stable version of FABRIC's libraries (`fablib`) and host stable Jupyter examples. It corresponds to the default container option on FABRIC's Jupyter Hub.

To start the `fabric-default` container:
1. Navigate to the release folder (for example, version `1.7.0`).
2. Run the following command to bring up the default container:
    ```bash
    cd 1.7.0
    docker-compose up -d fabric-default
    ```

#### 2. **fabric-bleeding**

This container runs the most up-to-date released version of `fablib` and includes the latest Jupyter examples. It corresponds to the "bleeding edge" container option on FABRIC's Jupyter Hub.

To start the `fabric-bleeding` container:
1. Navigate to the release folder (for example, version `1.7.0`).
2. Run the following command to bring up the bleeding edge container:
    ```bash
    cd 1.7.0
    docker-compose up -d fabric-bleeding
    ```

#### 3. **fabric-beyond-bleeding**

This is the most experimental container, running the `fablib` and Jupyter examples directly from the main branch. It includes the latest development changes and is primarily recommended for the FABRIC development team.

To start the `fabric-beyond-bleeding` container:
1. Navigate to the release folder (for example, version `1.7.0`).
2. Run the following command to bring up this development container:
    ```bash
    cd 1.7.0
    docker-compose up -d fabric-beyond-bleeding
    ```

### Important Notes:
- **Only one container can run at a time.** If you want to switch from one container to another, you will need to stop and remove the existing container before starting the new one. You can do this by running:
  ```bash
  docker-compose down
  docker-compose rm -fv
  ```
  Then, bring up the new container using the commands mentioned above.
  
- **Work Directory Mapping:** Each container maps the `~/work` directory on your local machine to the `/home/fabric/work` directory inside the container. This means that any work you do in the container is saved to your local machine, ensuring no data is lost when you switch or stop containers.

- **Token Setup:** Before running any notebooks, you need to download an authentication token from [FABRIC’s Credential Manager](https://cm.fabric-testbed.net/). Once you have the token, place it in your `~/work` directory on your machine. This step is necessary for authenticating your access to FABRIC resources.

By following these steps, you can easily switch between different FABRIC environments on your local machine while keeping your work saved.