# Dockerfile
FROM rockylinux:8
MAINTAINER Paul Ruth <pruth@renci.org>
LABEL maintainer="pruth@renci.org"

#ARG FABLIB_ENV=0.0.1


RUN echo "umask 0000" >> /etc/bashrc 


RUN  dnf install -y epel-release \
     && /usr/bin/crb enable \
     && dnf clean all \
     && rm -rf /var/cache/yum


# Basic tools
RUN dnf install -y  curl python3.9 python39-devel vim sudo git \
        && dnf groupinstall -y "Development Tools" \
        && dnf clean all \
        && rm -rf /var/cache/yum

# Install pip
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
        && python3 get-pip.py \
        && rm -rf get-pip.py


# Networking tools
RUN dnf install -y https://repos.fedorapeople.org/repos/openstack/openstack-yoga/rdo-release-yoga-1.el8.noarch.rpm \
        && dnf clean all \
        && rm -rf /var/cache/yum

# FABRIC Tools
RUN dnf install -y net-tools libibverbs  iputils iproute \
  	&& dnf clean all \
  	&& rm -rf /var/cache/yum

RUN python3.9 -m pip install --no-cache-dir fabrictestbed-extensions==1.4.1 \
                                            jupyter \
                                            jupyterlab \
                                            jupyter_contrib_nbextensions \
                                            nbconvert \
                                            paramiko \
                                            bash_kernel \
                                            scapy \
                                            ipywidgets \
                                            ipyleaflet \
                                            ipycytoscape \
                                            pandas \
                                            numpy \
                                            rpyc \
                                            python-openstackclient==5.6.2 \
                                            openstacksdk==0.59.0 \
                                            python-chi



RUN python3.9 -m pip install --no-cache-dir  pip install git+https://github.com/chameleoncloud/python-blazarclient@chameleoncloud/xena


RUN python3 -m bash_kernel.install

RUN useradd -ms /bin/bash fabric
RUN echo 'fabric ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

#RUN jupyter server --generate-config
#RUN jupyter server --generate-config
#jupyter server password


ADD work /home/fabric/work
RUN mkdir -p /home/fabric/work/fabric_config
RUN chown -R fabric:fabric /home/fabric/work

USER fabric
WORKDIR /home/fabric/work
RUN tar -zxvf jupyter-examples-rel1.4.3.tar.gz


# cleanup
RUN dnf clean all

ENV JUPYTER_LAB_PORT 8888

ENTRYPOINT jupyter lab --port $JUPYTER_LAB_PORT --NotebookApp.iopub_data_rate_limit=1.0e10 --no-browser --ip "*" --notebook-dir /home/fabric/work






