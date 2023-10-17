#!/bin/bash

docker stop $(docker ps -a -q)
./helper.sh new_admin
docker-compose up -d --build nginx


