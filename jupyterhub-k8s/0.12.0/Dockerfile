ARG BASE_JH=jupyterhub/k8s-hub:0.11.1-n146.hce40d36d
FROM $BASE_JH
COPY requirements.txt /srv/jupyterhub/requirements.txt
RUN pip3 install --no-cache-dir -r /srv/jupyterhub/requirements.txt

