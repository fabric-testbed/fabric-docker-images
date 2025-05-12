ARG BASE_JH=quay.io/jupyterhub/k8s-hub:4.2.0
FROM $BASE_JH
COPY requirements.txt /srv/jupyterhub/requirements.txt
RUN pip3 install --no-cache-dir -r /srv/jupyterhub/requirements.txt

