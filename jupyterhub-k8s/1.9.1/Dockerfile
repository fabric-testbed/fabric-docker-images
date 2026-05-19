ARG BASE_JH=quay.io/jupyterhub/k8s-hub:3.3.7
FROM $BASE_JH
COPY requirements.txt /srv/jupyterhub/requirements.txt
RUN pip3 install --no-cache-dir -r /srv/jupyterhub/requirements.txt

