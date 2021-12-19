FROM nikolaik/python-nodejs:python3.10-nodejs16-alpine

WORKDIR /usr/src/app

ENV FLASK_APP=rewritt/main.py

ENV FLASK_RUN_HOST=0.0.0.0

ENV NODE_VERSION=16.13.0

ENV NVM_DIR=/root/.nvm

COPY requirements.txt .

RUN apk add --no-cache \
      gcc \
      g++ \
      musl-dev \
      python3-dev \
      jpeg-dev \
      openjpeg-dev \
      zlib-dev \
      libffi-dev \
      openssl-dev \
      pango-dev \
      shared-mime-info \
      musl \
      jpeg \
      openjpeg \
      zlib \
      libffi \
      openssl \
      pango \
      ttf-opensans \
      ghostscript-fonts \
      tini

RUN pip install --user --no-cache-dir gunicorn

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN npm install -g pnpm

COPY ./rewritt ./rewritt

COPY ./bin ./bin

COPY ./client ./client

RUN mkdir static

WORKDIR /usr/src/app/client

RUN pnpm install && pnpm run build && mv ./build/** ../static

WORKDIR /usr/src/app

CMD ["flask", "run"]
