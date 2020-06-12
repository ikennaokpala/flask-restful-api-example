FROM python:3.7

ENV LSARP_DATABASE_URL=postgres://postgres:postgres@db:5432

RUN apt-get update -y && apt-get install sudo build-essential python3-dev libevent-dev libblas-dev libatlas-base-dev python3-venv make -y --no-install-recommends

WORKDIR /api

COPY entrypoint.sh /etc/entrypoint.sh
RUN chmod +x /etc/entrypoint.sh

COPY requirements.txt ./
COPY Makefile ./

RUN make install

EXPOSE 3000/tcp

