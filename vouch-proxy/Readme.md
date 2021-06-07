# Vouch Proxy
## Versions Available
- 0.27.1
## What is this?
Vouch Proxy (VP) forces visitors to login and authenticate with an IdP (such as one of the services listed above) before allowing them access to a website. Refer [here](https://github.com/vouch/vouch-proxy/blob/master/README.md) for more details.

This is a FABRIC specific image which allows refresh tokens to be passed in the HTTP headers.

Below is an example of docker-compose which allows creating vouch proxy:
```
   vouch-proxy:
     container_name: cm-vouch-proxy
     image: fabrictestbed/vouch-proxy:0.27.1
     volumes:
       - ./vouch:/config
       - ./data:/data
     restart: always
```
