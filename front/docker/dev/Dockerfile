FROM node:latest

ENV NODE_OPTIONS=--openssl-legacy-provider


ADD . /app
WORKDIR /app

EXPOSE 8080

COPY ./docker/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]

CMD [ "dev" ]