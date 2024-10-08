FROM quay.io/jupyterhub/singleuser:4.1.6 as base
ARG JUPYTERHUB_VERSION=4.1.6

USER root
RUN apt-get update --yes && \
  apt-get install --yes --no-install-recommends \
  # Common useful utilities
  file \
  git \
  nano-tiny \
  tzdata \
  unzip \
  vim-tiny \
  vim \
  curl \
  dnsutils \
  jq \
  tmux \
  less \
  moreutils \
  openssh-server \
  # git-over-ssh
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
  build-essential
RUN  apt-get clean && rm -rf /var/lib/apt/lists/*

ENV NEW_NB_USER=fabric
ENV HOME=/home/$NEW_NB_USER
RUN usermod --login $NEW_NB_USER --move-home --home $HOME $NB_USER
WORKDIR $HOME/work
ENV CHOWN_EXTRA=WORKDIR
ENV CHOWN_EXTRA_OPTS=-R
ENV GRANT_SUDO=yes

USER $NEW_NB_USER

RUN python3 -m pip install --no-cache-dir \
    jupyterhub==$JUPYTERHUB_VERSION

COPY requirements.txt /tmp/requirements.txt
COPY profile.sh /tmp/profile.sh

RUN python3 -m pip install --no-cache-dir -r /tmp/requirements.txt
RUN python3 -m pip install git+https://github.com/chameleoncloud/python-blazarclient.git@chameleoncloud/xena 

RUN python3 -m bash_kernel.install
RUN python3 -m sos_notebook.install
RUN python3 -m ansible_kernel.install

RUN echo 'eval "$(_FABRIC_CLI_COMPLETE=source_bash fabric-cli)"' >> ~/.bashrc

COPY release.txt /var/tmp/release.txt

# Add the disk space check script and make it executable
COPY check_disk_space.sh /var/tmp/check_disk_space.sh 


# Modify the PS1 environment variable in the .bashrc file to include release name
RUN echo 'release_name=$(cat /var/tmp/release.txt)' >> ~/.bashrc

# Customized shell prompt with username, release name, and disk space
RUN echo "PS1='\[\033[1;32m\]\u\[\033[0m\]@\[\033[1;30m\]\$release_name\[\033[0m\]:\[\033[1;35m\]\$(basename \"\$PWD\")\[\033[0m\]-\[\033[1;30m\]\$(df -h /home/fabric/work/ | awk \"NR==2 {print \\\$5}\")\[\033[0m\]$ '" >> ~/.bashrc


RUN echo '/var/tmp/check_disk_space.sh 60' >> ~/.bashrc


RUN sh /tmp/profile.sh

COPY jupyter_notebook_config.py /etc/jupyter/
USER root 

# To invoke gitpuller at start
COPY docker-entrypoint.sh /srv/docker-entrypoint.sh
RUN chmod 777 /srv/docker-entrypoint.sh
ENTRYPOINT ["tini", "--", "/srv/docker-entrypoint.sh"]
CMD ["start-singleuser.sh"]

USER $NEW_NB_USER
RUN mkdir -p $HOME/.ssh/
RUN ssh-keygen -b 2048 -t rsa -f $HOME/.ssh/id_rsa -q -N ""
RUN cp /etc/jupyter/jupyter_notebook_config.py /home/fabric/.jupyter/
