FROM jupyter/minimal-notebook:2fd856878b83
ARG JUPYTERHUB_VERSION=1.1.0
RUN python3 -m pip install --no-cache-dir \
    jupyterhub==$JUPYTERHUB_VERSION
COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install --no-cache-dir -r /tmp/requirements.txt
RUN python3 -m bash_kernel.install
RUN python3 -m sos_notebook.install
RUN jupyter labextension install transient-display-data
RUN jupyter labextension install jupyterlab-sos

# Install FABRIC CLI
RUN python3 -m pip install fabric_credmgr_client==0.0.3
RUN python3 -m pip install fabric-cli==0.5
RUN echo 'eval "$(_FABRIC_CLI_COMPLETE=source_bash fabric-cli)"' >> ~/.bashrc

# Change user name
USER root
ENV NEW_NB_USER=fabric
ENV HOME=/home/$NEW_NB_USER
RUN usermod --login $NEW_NB_USER --move-home --home $HOME $NB_USER
WORKDIR $HOME/work

# To invoke gitpuller at start
COPY docker-entrypoint.sh /srv/docker-entrypoint.sh
RUN chmod 777 /srv/docker-entrypoint.sh
ENTRYPOINT ["tini", "--", "/srv/docker-entrypoint.sh"]
CMD ["start-singleuser.sh"]

USER $NEW_NB_USER
