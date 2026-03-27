FROM ubuntu:latest as base

RUN apt-get update && apt-get install -y python3

FROM pwn.red/jail
COPY --from=base / /srv

RUN mkdir /srv/app
COPY src /srv/app
COPY src/assemble_run.sh /srv/app/run

ENV JAIL_MEM 100M
ENV JAIL_PIDS 50
ENV JAIL_PORT 1901
ENV JAIL_TMP_SIZE 10M
