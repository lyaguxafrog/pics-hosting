# -*- coding: utf-8 -*-


import telebot


import psycopg2
from psycopg2 import sql
import select

import os
from dotenv import load_dotenv, find_dotenv

from services.get_tokens import tokens

load_dotenv(find_dotenv())

dbname = os.getenv("POSTGRES_DB")
password = os.getenv("POSTGRES_PASSWORD")
user = os.getenv("POSTGRES_USER")

conn = psycopg2.connect(f"dbname={dbname} user={user} password={password} host=db port=5432")
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

cur = conn.cursor()

cur.execute("LISTEN new_token;")

while True:
    if select.select([conn], [], [], 5) == ([], [], []):
        pass
    else:
        conn.poll()
        while conn.notifies:
            notify = conn.notifies.pop(0)
            print("Received notification:", notify.payload)


            token_list = tokens()

            bots = []
            for token in token_list:
                bot = telebot.TeleBot(token)
                bots.append(bot)

                for bot in bots:
                    @bot.message_handler(func=lambda message: True)
                    def echo_all(message):
                        bot.reply_to(message, message.text)

            bot.polling()
