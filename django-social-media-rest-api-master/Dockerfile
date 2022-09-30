FROM continuumio/miniconda:latest

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

RUN apt-get update && apt-get install -y wget bzip2

COPY ./app/requirements.yml /app/requirements.yml
RUN conda env update -f /app/requirements.yml

COPY ./app /app

COPY ./scripts /scripts
RUN chmod +x /scripts/*

WORKDIR /app