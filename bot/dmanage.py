#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
from dotenv import load_dotenv, find_dotenv
from multiprocessing import Process

from bot.services.get_tokens import get_active_bot_tokens
from bot.bot_app import start_bot
from bot.services.db_connection import db

load_dotenv(find_dotenv())

bot_processes = {}

if __name__ == "__main__":
    while True:
        active_tokens = get_active_bot_tokens(db_connection=db())

        # Останавливаем процессы для токенов, которые стали неактивными
        for token, process in bot_processes.copy().items():
            if token not in active_tokens:
                process.terminate()
                del bot_processes[token]

        # Запускаем процессы для новых активных токенов
        for token in active_tokens:
            if token not in bot_processes:
                p = Process(target=start_bot, args=(token,))
                p.start()
                bot_processes[token] = p

        # Подождать некоторое время перед следующей проверкой базы данных
        time.sleep(int(os.getenv("UPDATE_TIME")))
