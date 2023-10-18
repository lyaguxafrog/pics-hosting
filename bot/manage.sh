#!/bin/bash


if [[ $1 == 'access' ]]; then
    sudo chown -R vscode .
    exit 0
fi

if [[ $1 == 'pip' ]]; then
    pip install -r requirements.txt
    rm -rf .devcontainer/requirements.txt
    cat requirements.txt  >> .devcontainer/requirements.txt
    exit 0
fi

python dmanage.py
