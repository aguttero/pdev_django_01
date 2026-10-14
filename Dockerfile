FROM python:3.14.8-alpine3.24
LABEL maintainer="github.com/aguttero"

ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000
