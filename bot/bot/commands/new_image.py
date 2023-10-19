# -*- coding: utf-8 -*-

import telebot
from telebot import types

import datetime

from bot.commands.start import handler_start

from bot.services.db_connection import db
from bot.services.last_login import last_login_update
from bot.services.ban_check import check_ban

con = db()
cur = con.cursor()

user_photos = {}

def pic_name_generator(user_id: str) -> str:
    """
    Функция генерации имен для изображений

    :param user_id: ID пользователя

    :return: Имя файла
    """
    date = str(datetime.datetime.now())
    file_name = f'imgs/{user_id}_{date}.png'
    return file_name


def handler_new_image(message, bot):
    telegram_id = str(message.from_user.id)

    if check_ban(user_id=telegram_id):
        bot.send_message(telegram_id, "У Вас нет доступа.")

    last_login_update(telegram_id=telegram_id)

    bot.send_message(telegram_id, "Отправьте изображение в виде файла.\n/cancel для отмены.")
    bot.register_next_step_handler(message, get_pic, bot)

def get_pic(message, bot):

    telegram_id = str(message.from_user.id)


    if message.text == '/cancel':
        bot.send_message(telegram_id, "Операция отменена")
        handler_start(message, bot)
        return

    elif message.photo:
        bot.send_message(telegram_id, "Пожалуйста, отправьте в виде файла.")
        bot.register_next_step_handler(message, get_pic, bot)

    elif message.document:

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        save_path =  pic_name_generator(user_id=telegram_id)  # сохраняем файл с его исходным именем
        with open(save_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        return
