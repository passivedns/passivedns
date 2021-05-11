FROM python:3

ARG VERSION
ENV VERSION=$VERSION

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "-u", "./main.py" ]
