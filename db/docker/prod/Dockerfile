FROM arangodb:latest

ARG ARANGO_ROOT_PASSWORD
ENV ARANGO_ROOT_PASSWORD=$ARANGO_ROOT_PASSWORD

COPY _init_db_tmp.js /docker-entrypoint-initdb.d/
