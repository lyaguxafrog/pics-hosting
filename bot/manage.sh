#!/bin/bash


if [[ $1 == 'access' ]]; then
    sudo chown -R vscode .
    exit 0
fi

python dmanage.py
