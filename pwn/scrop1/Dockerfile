FROM ubuntu:24.04 AS base
LABEL description="scrop1 challenge"

FROM pwn.red/jail
COPY --from=base / /srv

RUN mkdir /srv/app
COPY src/interpreter/interpreter /srv/app/run
#COPY a.out /srv/app/run
#RUN ln -s /bin/bash /srv/app/run
COPY src/flag.txt /srv/app/flag.txt

#RUN chmod 755 /srv/app/run
#RUN chmod 644 /srv/app/flag.txt

ENV JAIL_MEM 100M
ENV JAIL_PIDS 50
ENV JAIL_PORT 1900
