FROM ubuntu:24.04 AS base
LABEL description="scrop1 challenge"

RUN apt-get update

# install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
RUN mkdir -p /home/ubuntu/.cache/uv && chmod 777 /home/ubuntu/.cache/uv
ENV HOME=/tmp
ENV UV_CACHE_DIR=/tmp/uv_cache
RUN mkdir -p /tmp/uv_cache

FROM pwn.red/jail
COPY --from=base / /srv

RUN mkdir /srv/app

COPY src /srv/app
COPY src/interpreter/interpreter /srv/app/run

RUN chmod 755 /srv/app/run
RUN chmod 444 /srv/app/flag.txt

ENV JAIL_TIME 60
ENV JAIL_MEM 20M
ENV JAIL_POW 0

