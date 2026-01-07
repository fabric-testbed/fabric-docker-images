# PostgreSQL
## Versions Available
- 17.7 (Latest)
- 12.3
## What is this?
PostgreSQL, often simply "Postgres", is an object-relational database management system (ORDBMS) with an emphasis on extensibility and standards-compliance. Refer [here](https://github.com/docker-library/docs/blob/master/postgres/README.md) for more details.

This is a FABRIC specific image which allows multiple databases to be created in the same Postgres container.

Below is an example of docker-compose which allows creating an actorDb container with three databases:
```
     database:
         image: fabrictestbed/postgres:12.3
         container_name: actordb
         restart: always
         environment:
         - POSTGRES_PASSWORD=testpassword
         - POSTGRES_USER=testuser
         - POSTGRES_MULTIPLE_DATABASES=am,broker,controller
         ports:
         - "8432:5432"
```
