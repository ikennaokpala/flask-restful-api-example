FROM python:3.7

ENV SUDO='`which sudo`' LSARP_DATABASE_URL=postgres://postgres:postgres@db:5432

RUN apt-get update -y && apt-get install sudo build-essential python3-dev libevent-dev libblas-dev libatlas-base-dev make -y --no-install-recommends

WORKDIR /api

COPY requirements.txt ./
COPY Makefile ./
RUN make install

EXPOSE 3000/tcp
