ARG BASE_JH=jupyterhub/k8s-hub:0.9.0-n033.h8211ad2
FROM $BASE_JH
COPY requirements.txt /srv/jupyterhub/requirements.txt
RUN pip3 install --no-cache-dir -r /srv/jupyterhub/requirements.txt
RUN pip3 install --index-url https://test.pypi.org/simple/ -I fabricauthenticator

