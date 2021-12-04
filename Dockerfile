FROM python:3.10.0-alpine3.14

WORKDIR /usr/src/app

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

COPY ./rahool ./rahool
