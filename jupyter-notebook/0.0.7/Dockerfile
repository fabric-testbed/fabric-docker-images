FROM jupyter/minimal-notebook:hub-1.3.0
ARG JUPYTERHUB_VERSION=1.3.0
RUN python3 -m pip install --no-cache-dir \
    jupyterhub==$JUPYTERHUB_VERSION
COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install --no-cache-dir -r /tmp/requirements.txt
RUN python3 -m bash_kernel.install
RUN python3 -m sos_notebook.install
RUN python3 -m pip install ipympl
RUN jupyter labextension install transient-display-data
RUN jupyter labextension install jupyterlab-sos
RUN jupyter labextension install @jupyter-widgets/jupyterlab-manager
RUN jupyter labextension install jupyter-matplotlib
RUN python3 -m pip install paramiko
# Install FABRIC CLI
RUN python3 -m pip install fabric-fim==0.40 fabric-orchestrator-client==0.0.15 fabric-cli==0.8
RUN echo 'eval "$(_FABRIC_CLI_COMPLETE=source_bash fabric-cli)"' >> ~/.bashrc

# Change user name
USER root
RUN apt-get clean
RUN apt-get update
RUN apt-get install -yq openssh-server
ENV NEW_NB_USER=fabric
ENV HOME=/home/$NEW_NB_USER
RUN usermod --login $NEW_NB_USER --move-home --home $HOME $NB_USER
WORKDIR $HOME/work
ENV CHOWN_EXTRA=WORKDIR
ENV CHOWN_EXTRA_OPTS=-R
ENV GRANT_SUDO=yes

# To invoke gitpuller at start
COPY docker-entrypoint.sh /srv/docker-entrypoint.sh
RUN chmod 777 /srv/docker-entrypoint.sh
ENTRYPOINT ["tini", "--", "/srv/docker-entrypoint.sh"]
CMD ["start-singleuser.sh"]

USER $NEW_NB_USER
RUN mkdir $HOME/.ssh/
RUN ssh-keygen -b 2048 -t rsa -f $HOME/.ssh/id_rsa -q -N ""
