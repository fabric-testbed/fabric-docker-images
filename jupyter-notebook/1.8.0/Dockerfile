# Base Image
FROM quay.io/jupyterhub/singleuser:4.1.6 as base
ARG JUPYTERHUB_VERSION=4.1.6

USER root

# Combine apt-get update and install in a single RUN command and clean up afterwards
RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends \
        file \
        git \
        nano-tiny \
        tzdata \
        unzip \
        vim-tiny \
        curl \
        dnsutils \
        jq \
        tmux \
        less \
        moreutils \
        openssh-server \
        openssh-client \
        gcc \
        gpa \
        seahorse \
        iputils-ping \
        traceroute \
        iproute2 \
        net-tools \
        tcpdump \
        netcat \
        build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set up user and environment
ENV NEW_NB_USER=fabric
ENV HOME=/home/$NEW_NB_USER
RUN usermod --login $NEW_NB_USER --move-home --home $HOME $NB_USER
WORKDIR $HOME/work
ENV CHOWN_EXTRA=WORKDIR
ENV CHOWN_EXTRA_OPTS=-R
ENV GRANT_SUDO=yes

# Switch to the new user
USER $NEW_NB_USER

# Install Python packages without cache
RUN python3 -m pip install --no-cache-dir jupyterhub==$JUPYTERHUB_VERSION

# Copy requirements and profile scripts
COPY requirements.txt /tmp/requirements.txt
COPY profile.sh /tmp/profile.sh

# Install requirements from requirements.txt
RUN python3 -m pip install --no-cache-dir -r /tmp/requirements.txt && \
    python3 -m pip install --no-cache-dir git+https://github.com/chameleoncloud/python-blazarclient.git@chameleoncloud/xena

# Install additional kernels
RUN python3 -m bash_kernel.install && \
    python3 -m sos_notebook.install && \
    python3 -m ansible_kernel.install

# Configure shell environment
RUN echo 'eval "$(_FABRIC_CLI_COMPLETE=source_bash fabric-cli)"' >> ~/.bashrc && \
    echo 'release_name=$(cat /var/tmp/release.txt)' >> ~/.bashrc && \
    echo "PS1='\[\033[1;32m\]\u\[\033[0m\]@\[\033[1;30m\]\$release_name\[\033[0m\]:\[\033[1;35m\]\$(basename \"\$PWD\")\[\033[0m\]-\[\033[1;30m\]\$(df -h /home/fabric/work/ | awk \"NR==2 {print \\\$5}\")\[\033[0m\]$ '" >> ~/.bashrc && \
    echo '/var/tmp/check_disk_space.sh 60' >> ~/.bashrc

# Copy the release file and disk space check script
COPY release.txt /var/tmp/release.txt
COPY check_disk_space.sh /var/tmp/check_disk_space.sh

# Run profile script
RUN sh /tmp/profile.sh

# Copy Jupyter Notebook configuration
COPY jupyter_notebook_config.py /etc/jupyter/
USER root

# Copy entrypoint script and set permissions
COPY docker-entrypoint.sh /srv/docker-entrypoint.sh
RUN chmod +x /srv/docker-entrypoint.sh

# Define entrypoint and command
ENTRYPOINT ["tini", "--", "/srv/docker-entrypoint.sh"]
CMD ["start-singleuser.sh"]

# Set user back to the new user
USER $NEW_NB_USER
RUN mkdir -p $HOME/.ssh/ && \
    ssh-keygen -b 2048 -t rsa -f $HOME/.ssh/id_rsa -q -N "" && \
    cp /etc/jupyter/jupyter_notebook_config.py /home/fabric/.jupyter/

