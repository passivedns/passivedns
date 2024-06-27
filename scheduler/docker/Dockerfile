FROM python:3.12

ARG VERSION
ENV VERSION=$VERSION

RUN apt-get update && apt-get install -y \
    python3-pip \
    libmagic-dev \
    git \
    && apt-get clean && rm -rf /var/cache/apt/* /var/lib/apt/lists/*

ADD . /app
WORKDIR /app

RUN cp ./scheduler/docker/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

RUN pip3 install --upgrade pip && pip3 install poetry

RUN poetry install --no-dev

ENV PYTHONPATH /app

ENTRYPOINT ["/docker-entrypoint.sh"]

CMD ["scheduler"]
