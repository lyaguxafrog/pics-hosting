#!/bin/bash

PROJECT=${PWD##*/}

if [[ $1 = 'config' ]]; then

    cat ./kernel/.env.example >> ./kernel/.env
    echo "Обязательно смените SECRET_KEY"
    echo "Используйте https://djecrety.ir/"
    cat ./kernel/config/local_settings.example >> ./kernel/config/local_settings.py

fi


if [[ $1 = 'startapp' ]]; then

    echo "Starting..."
    docker-compose up -d --build db
    docker-compose up -d --build kernel
    # docker-compose up -d --build bot





fi

if [[ $1 = 'clear' ]]; then

    docker stop $(docker ps -a -q)
    docker system prune -a

    exit 0

fi
