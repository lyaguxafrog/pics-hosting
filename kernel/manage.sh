#!/bin/bash


if [[ $1 = 'sql' ]]; then
    ./dmanage.py sql
    exit 0
fi

if [[ $1 = 'su' ]]; then
    ./dmanage.py su
    exit 0
fi

if [[ $1 = 'pip' ]]; then
    pip install -r requirements.txt
    cat  requirements.txt >> .devcontainer/requirements.txt
    exit 0
fi

if [[ $1 = 'su_admin' ]]; then
    ./dmanage.py sa
    exit 0

fi

./dmanage.py $@
