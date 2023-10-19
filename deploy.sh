#!/bin/bash



if [[ $1 = 'update' ]]; then
    docker-compose up -d --build nginx
fi


./helper.sh new_admin
docker-compose up -d --build nginx

