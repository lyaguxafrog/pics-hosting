# -*- coding: utf-8 -*-

import psycopg2
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

def db():
    """
    Функция подключения к БД

    :return: Коннект к БД
    """
    db_connection = psycopg2.connect(
        host="db",
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )

    return db_connection
