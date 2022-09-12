# JupyterHub 2.0.0
FROM jupyterhub/singleuser:2.0.0 as base
ARG JUPYTERHUB_VERSION=1.3.0
ARG FABRIC_CLI=1.3.0
ARG FABRIC_CLI_EXT=1.3.0

USER root
RUN apt-get update --yes && \
  apt-get install --yes --no-install-recommends \
  # Common useful utilities
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
  # git-over-ssh
  openssh-client \
  gcc \
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
COPY jupyter_startup.py /var/tmp

RUN python3 -m pip install --no-cache-dir -r /tmp/requirements.txt
RUN python3 -m pip install git+https://github.com/chameleoncloud/python-blazarclient.git@chameleoncloud/xena 

RUN python3 -m bash_kernel.install
RUN python3 -m sos_notebook.install
RUN python3 -m ansible_kernel.install

RUN jupyter labextension install transient-display-data
RUN jupyter labextension install jupyterlab-sos
RUN jupyter labextension install @jupyter-widgets/jupyterlab-manager
RUN jupyter labextension install jupyter-matplotlib

# Install FABRIC CLI
RUN python3 -m pip install fabrictestbed==${FABRIC_CLI}
RUN python3 -m pip install fabrictestbed-extensions==${FABRIC_CLI_EXT}
RUN echo 'eval "$(_FABRIC_CLI_COMPLETE=source_bash fabric-cli)"' >> ~/.bashrc

USER root 

# To invoke gitpuller at start
COPY docker-entrypoint.sh /srv/docker-entrypoint.sh
RUN chmod 777 /srv/docker-entrypoint.sh
ENTRYPOINT ["tini", "--", "/srv/docker-entrypoint.sh"]
CMD ["start-singleuser.sh"]

USER $NEW_NB_USER
RUN mkdir -p $HOME/.ssh/
RUN ssh-keygen -b 2048 -t rsa -f $HOME/.ssh/id_rsa -q -N ""
