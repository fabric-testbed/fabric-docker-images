ARG BASE_JH=jupyterhub/k8s-hub:2.0.0
FROM $BASE_JH
COPY requirements.txt /srv/jupyterhub/requirements.txt
RUN pip3 install --no-cache-dir -r /srv/jupyterhub/requirements.txt

