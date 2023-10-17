# -*- coding: utf-8 -*-

import psycopg2

import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

import psycopg2

def tokens() -> list:
    """
    Функция получения токенов из БД

    :return: list токенов
    """

    active_bot_tokens = []

    dbname = os.getenv("POSTGRES_DB")
    password = os.getenv("POSTGRES_PASSWORD")
    user = os.getenv("POSTGRES_USER")

    connection_string = f"dbname={dbname} user={user} password={password} host=db port=5432"

    try:
        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor()

        # Выбираем все bot_token из таблицы bot, где is_active равно True
        cursor.execute("SELECT bot_token FROM bot WHERE is_active = True")

        # Получаем результаты запроса в виде списка кортежей
        results = cursor.fetchall()

        # Извлекаем bot_token из кортежей и добавляем их в список active_bot_tokens
        for result in results:
            active_bot_tokens.append(result[0])

        conn.close()
    except psycopg2.Error as e:
        print("Ошибка при выполнении SQL-запроса:", e)

    print(active_bot_tokens)
    return active_bot_tokens
