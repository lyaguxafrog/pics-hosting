import telebot
import psycopg2
from multiprocessing import Process
import time

import os
from dotenv import load_dotenv, find_dotenv


# Подключение к базе данных PostgreSQL
db_connection = psycopg2.connect(
    host="db",
    database=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
)

# Глобальный словарь для хранения процессов ботов
bot_processes = {}

# Функция для получения списка активных токенов из базы данных
def get_active_bot_tokens():
    cursor = db_connection.cursor()
    cursor.execute("SELECT bot_token FROM bot WHERE is_active = true;")
    tokens = {row[0] for row in cursor.fetchall()}
    cursor.close()
    return tokens

# Функция, которая будет выполняться для каждого активного бота
def start_bot(token):
    bot_instance = telebot.TeleBot(token)

    @bot_instance.message_handler(func=lambda message: True)
    def echo_all(message):
        bot_instance.reply_to(message, message.text)

    bot_instance.polling(none_stop=True)

if __name__ == "__main__":
    while True:
        active_tokens = get_active_bot_tokens()

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
        time.sleep(int(os.getenv("UPDATE_TIME")))  # Например, каждые 5 минут (300 секунд)
