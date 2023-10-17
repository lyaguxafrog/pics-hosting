import telebot
import psycopg2

import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Функция для установления соединения с базой данных и получения активных токенов
def get_active_bot_tokens():
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host="db",
    )
    cursor = conn.cursor()
    cursor.execute("SELECT bot_token FROM bot WHERE is_active = TRUE")
    active_tokens = [row[0] for row in cursor.fetchall()]
    conn.close()
    return active_tokens

# Создаем ботов на основе активных токенов
active_tokens = get_active_bot_tokens()
bots = [telebot.TeleBot(token) for token in active_tokens]

# Функция для обработки команды /start
def handle_start(message):
    for bot in bots:
        bot.send_message(message.chat.id, "Привет, я активен!")

# Создаем хендлер для команды /start для каждого бота
for bot in bots:
    @bot.message_handler(commands=['start'])
    def start(message):
        handle_start(message)

if __name__ == "__main__":
    for bot in bots:
        bot.remove_webhook()
        bot.polling(none_stop=True)
