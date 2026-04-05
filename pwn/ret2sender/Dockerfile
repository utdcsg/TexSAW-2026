# our local base image
FROM ubuntu:24.04 AS base
LABEL description="Container for Ubuntu-24"

FROM pwn.red/jail
COPY --from=base / /srv

RUN mkdir /srv/app
COPY src/chall /srv/app/run
COPY src/flag.txt /srv/app/flag.txt

RUN chmod 755 /srv/app/run
RUN chmod 644 /srv/app/flag.txt

ENV JAIL_TIME 60
ENV JAIL_MEM 10M
