FROM python:3

ARG ARANGO_USERNAME
ARG ARANGO_PASSWORD
ARG DB_HOST
ARG DB_NAME
ARG JWT_SECRET_KEY

ARG VERSION
ARG JOB_URL
ARG COMMIT_SHA

ARG TIMEZONE



ENV ARANGO_USERNAME=$ARANGO_USERNAME
ENV ARANGO_PASSWORD=$ARANGO_PASSWORD
ENV DB_HOST = $DB_HOST
ENV DB_NAME = $DB_NAME 
ENV JWT_SECRET_KEY=$JWT_SECRET_KEY

ENV VERSION=$VERSION
ENV JOB_URL=$JOB_URL
ENV COMMIT_SHA=$COMMIT_SHA

ENV TIMEZONE=$TIMEZONE
RUN apt-get update && apt-get install -y \
    python3-pip \
    libmagic-dev \
    git \
    && apt-get clean && rm -rf /var/cache/apt/* /var/lib/apt/lists/*

ADD . /app
WORKDIR /app

COPY --chmod=744 extras/docker/docker-entrypoint.sh /docker-entrypoint.sh

RUN pip3 install --upgrade pip && pip3 install poetry

RUN poetry install --no-root

ENV PYTHONPATH /app
CMD ["webserver"]

