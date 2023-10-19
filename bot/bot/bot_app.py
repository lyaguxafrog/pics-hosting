import os
import telebot
from telebot import types
import requests
from datetime import datetime
from bot.models import TelegramUser, Picture

from bot.services.get_tokens import get_active_bot_tokens
from bot.services.db_connection import db

from bot.commands.start import handler_start

# Функция для получения списка активных токенов из базы данных
tokens = get_active_bot_tokens(db_connection=db())


conn = db()
cursor = conn.cursor()



user_data = {}

# Функция, которая будет выполняться для каждого активного бота
def start_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start'])
    def start(mesage):
        handler_start(mesage, bot)

    # Запускаем бот
    bot.remove_webhook()
    bot.polling(none_stop=True)
