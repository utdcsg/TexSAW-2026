FROM ubuntu:24.04 AS base
LABEL description="Whats The Time Challenge"

# Install 32-bit libraries
RUN dpkg --add-architecture i386 && \
    apt-get update && \
    apt-get install -y libc6:i386 && \
    rm -rf /var/lib/apt/lists/*

FROM pwn.red/jail
COPY --from=base / /srv

RUN mkdir /srv/app

COPY src/whatsthetime /srv/app/run
COPY src/flag.txt /srv/app/flag.txt

RUN chmod 755 /srv/app/run
RUN chmod 444 /srv/app/flag.txt

ENV JAIL_TIME 60
ENV JAIL_MEM 20M
ENV JAIL_POW 0
