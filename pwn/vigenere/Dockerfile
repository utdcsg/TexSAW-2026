FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    gcc \
    socat \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -d /home/ctf/ -m -p ctf -s /bin/bash ctf
WORKDIR /home/ctf

COPY vigenere.c .

RUN echo "texsaw{wRit3a61e_X0R_exECutA61e}" > flag.txt

RUN gcc -fcf-protection=return -z execstack -o vigenere_executeable vigenere.c

RUN chown -R root:ctf /home/ctf && \
    chmod -R 750 /home/ctf && \
    chmod 740 /home/ctf/flag.txt