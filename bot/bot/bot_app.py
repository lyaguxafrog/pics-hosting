import telebot


import psycopg2
from multiprocessing import Process
import time
import os
from dotenv import load_dotenv, find_dotenv


from bot.services.get_tokens import get_active_bot_tokens
from bot.services.dbconnect import db


# Функция для получения списка активных токенов из базы данных
tokens = get_active_bot_tokens(db_connection=db())

# Функция, которая будет выполняться для каждого активного бота
def start_bot(token):
    bot_instance = telebot.TeleBot(token)

    @bot_instance.message_handler(func=lambda message: True)
    def echo_all(message):
        bot_instance.reply_to(message, message.text)

    bot_instance.polling(none_stop=True)
