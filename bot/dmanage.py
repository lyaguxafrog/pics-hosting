#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telebot
from telebot import types

from sqlalchemy import create_engine, Column, Integer, String, Text, Date, Boolean, LargeBinary
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import datetime

import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


username = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
dbname = os.getenv("POSTGRES_DB")

engine = create_engine(f'postgresql://{username}:{password}@localhost/{dbname}')  # Замените параметры подключения
Session = sessionmaker(bind=engine)
Base = declarative_base()

Base.metadata.create_all(engine)

TOKEN = os.getenv("MAIN_BOT")  # main
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user = TelegramUser(telegram_id=chat_id, reg_date=datetime.date.today())
    session = Session()
    session.add(user)
    session.commit()
    bot.send_message(chat_id, "Добро пожаловать! Вы зарегистрированы.")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    chat_id = message.chat.id
    user = session.query(TelegramUser).filter_by(telegram_id=chat_id).first()
    if user.is_banned:
        bot.send_message(chat_id, "Вы заблокированы и не можете загружать картинки.")
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item_name = types.KeyboardButton("Введите имя картинки")
    item_password = types.KeyboardButton("Введите пароль (или нажмите 'Пропустить')")
    item_one_view = types.KeyboardButton("Установить режим просмотра (один раз)")
    markup.add(item_name, item_password, item_one_view)

    bot.send_message(chat_id, "Отлично! Теперь давайте настроим вашу картинку.", reply_markup=markup)
    bot.register_next_step_handler(message, handle_picture_settings)

def handle_picture_settings(message):
    chat_id = message.chat.id
    user = session.query(TelegramUser).filter_by(telegram_id=chat_id).first()
    if user.is_banned:
        bot.send_message(chat_id, "Вы заблокированы и не можете загружать картинки.")
        return

    if message.text == "Отмена":
        bot.send_message(chat_id, "Загрузка картинки отменена.")
        return

    if user.pics_count is None:
        user.pics_count = 0

    if message.text == "Введите имя картинки":
        bot.send_message(chat_id, "Введите имя картинки:")
        bot.register_next_step_handler(message, set_picture_name)
    elif message.text == "Введите пароль (или нажмите 'Пропустить')":
        bot.send_message(chat_id, "Введите пароль (или нажмите 'Пропустить'):")
        bot.register_next_step_handler(message, set_picture_password)
    elif message.text == "Установить режим просмотра (один раз)":
        bot.send_message(chat_id, "Установить режим просмотра (один раз)?", reply_markup=types.ReplyKeyboardRemove())
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        item_yes = types.KeyboardButton("Да")
        item_no = types.KeyboardButton("Нет")
        markup.add(item_yes, item_no)
        bot.send_message(chat_id, "Установить режим просмотра (один раз)?", reply_markup=markup)
        bot.register_next_step_handler(message, set_picture_one_view)
    else:
        bot.send_message(chat_id, "Пожалуйста, используйте кнопки для настройки картинки.")


def set_picture_name(message):
    chat_id = message.chat.id
    user = session.query(TelegramUser).filter_by(telegram_id=chat_id).first()
    if user.is_banned:
        bot.send_message(chat_id, "Вы заблокированы и не можете загружать картинки.")
        return

    user.pics_count += 1
    picture = Pictures(name=message.text, owner_id=chat_id)
    session = Session()
    session.add(picture)
    session.commit()
    bot.send_message(chat_id, "Имя картинки установлено. Теперь отправьте саму картинку.")

@bot.message_handler(func=lambda message: True, content_types=['photo'])
def handle_uploaded_photo(message):
    chat_id = message.chat.id
    user = session.query(TelegramUser).filter_by(telegram_id=chat_id).first()
    if user.is_banned:
        bot.send_message(chat_id, "Вы заблокированы и не можете загружать картинки.")
        return

    picture = session.query(Pictures).filter_by(owner_id=chat_id, pic_data=None).order_by(Pictures.id.desc()).first()
    if picture is not None:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        file = bot.download_file(file_info.file_path)
        picture.pic_data = file.read()
        session.commit()
        bot.send_message(chat_id, "Картинка загружена. Вы можете поделиться ей по следующей ссылке:")
        bot.send_photo(chat_id, file_id, caption=f"Название: {picture.name}\nПароль: {picture.password}\n"
                                                f"Режим просмотра: {'Один раз' if picture.is_one_view else 'Без ограничений'}")
    else:
        bot.send_message(chat_id, "Произошла ошибка при загрузке картинки. Попробуйте снова.")


def set_picture_password(message):
    chat_id = message.chat.id
    user = session.query(TelegramUser).filter_by(telegram_id=chat_id).first()
    if user.is_banned:
        bot.send_message(chat_id, "Вы заблокированы и не можете загружать картинки.")
        return

    text = message.text
    picture = session.query(Pictures).filter_by(owner_id=chat_id, password=None).order_by(Pictures.id.desc()).first()
    if text.lower() == "пропустить":
        picture.password = None
    else:
        picture.password = text
    session.commit()
    bot.send_message(chat_id, "Пароль установлен.")


def set_picture_one_view(message):
    chat_id = message.chat.id
    user = session.query(TelegramUser).filter_by(telegram_id=chat_id).first()
    if user.is_banned:
        bot.send_message(chat_id, "Вы заблокированы и не можете загружать картинки.")
        return

    text = message.text
    picture = session.query(Pictures).filter_by(owner_id=chat_id, is_one_view=None).order_by(Pictures.id.desc()).first()
    if text.lower() == "да":
        picture.is_one_view = True
    elif text.lower() == "нет":
        picture.is_one_view = False
    else:
        bot.send_message(chat_id, "Пожалуйста, используйте кнопки 'Да' или 'Нет'.")
        return
    session.commit()
    bot.send_message(chat_id, "Режим просмотра установлен.")


@bot.message_handler(commands=['my_pictures'])
def my_pictures(message):
    chat_id = message.chat.id
    user = session.query(TelegramUser).filter_by(telegram_id=chat_id).first()
    if user.is_banned:
        bot.send_message(chat_id, "Вы заблокированы и не можете просматривать свои картинки.")
        return

    pictures = session.query(Pictures).filter_by(owner_id=chat_id).all()
    if pictures:
        for picture in pictures:
            bot.send_message(chat_id, f"Имя: {picture.name}\n"
                                      f"Пароль: {picture.password if picture.password else 'Отсутствует'}\n"
                                      f"Режим просмотра: {'Один раз' if picture.is_one_view else 'Без ограничений'}\n"
                                      f"Просмотры: {picture.view}")
    else:
        bot.send_message(chat_id, "У вас пока нет загруженных картинок.")


@bot.message_handler(commands=['set_password'])
def set_password(message):
    chat_id = message.chat.id
    user = session.query(TelegramUser).filter_by(telegram_id=chat_id).first()
    if user.is_banned:
        bot.send_message(chat_id, "Вы заблокированы и не можете устанавливать пароль для картинок.")
        return

    pictures = session.query(Pictures).filter_by(owner_id=chat_id).all()
    if pictures:
        bot.send_message(chat_id, "Выберите картинку, для которой нужно установить пароль:", reply_markup=get_pictures_markup(pictures))
        bot.register_next_step_handler(message, handle_set_password)
    else:
        bot.send_message(chat_id, "У вас пока нет загруженных картинок.")

def get_pictures_markup(pictures):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for picture in pictures:
        markup.add(types.KeyboardButton(picture.name))
    markup.add(types.KeyboardButton("Отмена"))
    return markup

def handle_set_password(message):
    chat_id = message.chat.id
    user = session.query(TelegramUser).filter_by(telegram_id=chat_id).first()
    if user.is_banned:
        bot.send_message(chat_id, "Вы заблокированы и не можете устанавливать пароль для картинок.")
        return

    text = message.text
    if text == "Отмена":
        bot.send_message(chat_id, "Установка пароля отменена.")
        return

    picture = session.query(Pictures).filter_by(owner_id=chat_id, name=text).first()
    if picture:
        bot.send_message(chat_id, "Введите новый пароль для этой картинки:")
        bot.register_next_step_handler(message, set_new_password, picture)
    else:
        bot.send_message(chat_id, "Не найдено картинки с таким именем. Попробуйте снова.")

def set_new_password(message, picture):
    chat_id = message.chat.id
    user = session.query(TelegramUser).filter_by(telegram_id=chat_id).first()
    if user.is_banned:
        bot.send_message(chat_id, "Вы заблокированы и не можете устанавливать пароль для картинок.")
        return

    text = message.text
    picture.password = text
    session.commit()
    bot.send_message(chat_id, "Пароль установлен для этой картинки.")

@bot.message_handler(commands=['remove_password'])
def remove_password(message):
    chat_id = message.chat.id
    user = session.query(TelegramUser).filter_by(telegram_id=chat_id).first()
    if user.is_banned:
        bot.send_message(chat_id, "Вы заблокированы и не можете удалять пароль для картинок.")
        return

    pictures = session.query(Pictures).filter_by(owner_id=chat_id).all()
    if pictures:
        bot.send_message(chat_id, "Выберите картинку, у которой нужно удалить пароль:", reply_markup=get_pictures_markup(pictures))
        bot.register_next_step_handler(message, handle_remove_password)
    else:
        bot.send_message(chat_id, "У вас пока нет загруженных картинок.")

def handle_remove_password(message):
    chat_id = message.chat.id
    user = session.query(TelegramUser).filter_by(telegram_id=chat_id).first()
    if user.is_banned:
        bot.send_message(chat_id, "Вы заблокированы и не можете удалять пароль для картинок.")
        return

    text = message.text
    if text == "Отмена":
        bot.send_message(chat_id, "Удаление пароля отменено.")
        return

    picture = session.query(Pictures).filter_by(owner_id=chat_id, name=text).first()
    if picture:
        picture.password = None
        session.commit()
        bot.send_message(chat_id, "Пароль удален для этой картинки.")
    else:
        bot.send_message(chat_id, "Не найдено картинки с таким именем. Попробуйте снова.")

@bot.message_handler(commands=['set_one_view'])
def set_one_view(message):
    chat_id = message.chat.id
    user = session.query(TelegramUser).filter_by(telegram_id=chat_id).first()
    if user.is_banned:
        bot.send_message(chat_id, "Вы заблокированы и не можете устанавливать режим просмотра для картинок.")
        return

    pictures = session.query(Pictures).filter_by(owner_id=chat_id).all()
    if pictures:
        bot.send_message(chat_id, "Выберите картинку, для которой нужно установить режим просмотра:", reply_markup=get_pictures_markup(pictures))
        bot.register_next_step_handler(message, handle_set_one_view)
    else:
        bot.send_message(chat_id, "У вас пока нет загруженных картинок.")

def handle_set_one_view(message):
    chat_id = message.chat.id
    user = session.query(TelegramUser).filter_by(telegram_id=chat_id).first()
    if user.is_banned:
        bot.send_message(chat_id, "Вы заблокированы и не можете устанавливать режим просмотра для картинок.")
        return

    text = message.text
    if text == "Отмена":
        bot.send_message(chat_id, "Установка режима просмотра отменена.")
        return

    picture = session.query(Pictures).filter_by(owner_id=chat_id, name=text).first()
    if picture:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        item_one_view = types.KeyboardButton("Установить режим просмотра (один раз)")
        item_unlimited_view = types.KeyboardButton("Отменить режим просмотра (без ограничений)")
        markup.add(item_one_view, item_unlimited_view)
        bot.send_message(chat_id, "Выберите режим просмотра для этой картинки:", reply_markup=markup)
        bot.register_next_step_handler(message, set_picture_one_view, picture)
    else:
        bot.send_message(chat_id, "Не найдено картинки с таким именем. Попробуйте снова.")


@bot.message_handler(commands=['remove_one_view'])
def remove_one_view(message):
    chat_id = message.chat.id
    user = session.query(TelegramUser).filter_by(telegram_id=chat_id).first()
    if user.is_banned:
        bot.send_message(chat_id, "Вы заблокированы и не можете удалять режим просмотра для картинок.")
        return

    pictures = session.query(Pictures).filter_by(owner_id=chat_id).all()
    if pictures:
        bot.send_message(chat_id, "Выберите картинку, у которой нужно удалить режим просмотра:", reply_markup=get_pictures_markup(pictures))
        bot.register_next_step_handler(message, handle_remove_one_view)
    else:
        bot.send_message(chat_id, "У вас пока нет загруженных картинок.")

def handle_remove_one_view(message):
    chat_id = message.chat.id
    user = session.query(TelegramUser).filter_by(telegram_id=chat_id).first()
    if user.is_banned:
        bot.send_message(chat_id, "Вы заблокированы и не можете удалять режим просмотра для картинок.")
        return

    text = message.text
    if text == "Отмена":
        bot.send_message(chat_id, "Удаление режима просмотра отменено.")
        return

    picture = session.query(Pictures).filter_by(owner_id=chat_id, name=text).first()
    if picture:
        picture.is_one_view = None
        session.commit()
        bot.send_message(chat_id, "Режим просмотра удален для этой картинки.")
    else:
        bot.send_message(chat_id, "Не найдено картинки с таким именем. Попробуйте снова.")

@bot.message_handler(commands=['ban'])
def ban_user(message):
    chat_id = message.chat.id
    user = session.query(TelegramUser).filter_by(telegram_id=chat_id).first()
    if user.is_banned:
        bot.send_message(chat_id, "Вы уже заблокированы.")
    else:
        user.is_banned = True
        session.commit()
        bot.send_message(chat_id, "Вы заблокированы. Вы не сможете использовать бота.")

@bot.message_handler(commands=['unban'])
def unban_user(message):
    chat_id = message.chat.id
    user = session.query(TelegramUser).filter_by(telegram_id=chat_id).first()
    if user.is_banned:
        user.is_banned = False
        session.commit()
        bot.send_message(chat_id, "Вы разблокированы. Теперь вы можете использовать бота.")
    else:
        bot.send_message(chat_id, "Вы не заблокированы.")


if __name__ == '__main__':
    bot.polling(none_stop=True)
