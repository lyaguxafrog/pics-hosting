#!/bin/bash

PROJECT=${PWD##*/}

if [[ $1 = 'config' ]]; then

    cat ./kernel/.env.example >> ./kernel/.env
    rm -rf README.md
    cat ./bot/.env.example >> ./bot/.env

    echo "Обязательно смените SECRET_KEY"
    echo "Используйте https://djecrety.ir/"
fi


if [[ $1 = 'startapp' ]]; then

    echo "Starting..."
    docker-compose up -d --build db
    docker-compose up -d --build kernel
    docker-compose up -d --build bot
    docker-compose up -d --build nginx
fi

if [[ $1 = 'new_admin' ]]; then

    docker-compose up -d --build kernel
    docker exec ${PROJECT}_kernel_1 ./manage.sh
    docker-compose down

    docker-compose up -d --build kernel
    docker exec ${PROJECT}_kernel_1 ./manage.sh sa
    docker-compose down



fi

if [[ $1 = 'clear' ]]; then

    docker stop $(docker ps -a -q)
    docker system prune -a

    exit 0

fi
