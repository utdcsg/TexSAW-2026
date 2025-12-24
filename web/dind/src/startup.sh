#!/bin/sh
mkdir -p /flag 
apk add --no-cache docker-compose bash py3-pip

dockerd-entrypoint.sh &

#echo '****************Waiting for Docker daemon to start...' 
#until docker info >/dev/null 2>&1; do
#    sleep 1
#done 
#echo '******************Docker daemon started successfully!' 
sleep 25

cd /workspace 

export DOCKER_HOST=unix:///var/run/docker.sock

docker-compose build 
docker-compose up -d 
tail -f /dev/null
