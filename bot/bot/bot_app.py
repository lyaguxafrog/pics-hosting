import telebot
import psycopg2
from multiprocessing import Process
from datetime import datetime
from PIL import Image
import io
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.services.get_tokens import get_active_bot_tokens
from bot.services.dbconnect import db
from bot.services.last_login import update_last_login
from bot.services.saveimage import save_image
import psycopg2
from psycopg2 import sql
from io import BytesIO


# Функция для получения списка активных токенов из базы данных
tokens = get_active_bot_tokens(db_connection=db())

datebase = db()
db_cursor = datebase.cursor()


# Функция для сохранения изображения в базе данных с использованием Large Objects
def save_image(user_id, name, password, image_data):
    try:
        conn = db()
        cursor = conn.cursor()

        # Создать новый Large Object
        cursor.execute("SELECT lo_create(0)")
        image_oid = cursor.fetchone()[0]

        # Откройте Large Object для записи
        cursor.execute(sql.SQL("SELECT lo_open(%s, %s)"), (image_oid, psycopg2.extensions.LO_WRONLY))
        image_file = cursor.fetchone()[0]

        # Запишите данные изображения в Large Object
        image_data_stream = BytesIO(image_data)
        while True:
            data = image_data_stream.read(1024)
            if not data:
                break
            cursor.execute(sql.SQL("SELECT lowrite(%s, %s)"), (image_file, psycopg2.Binary(data)))

        # Закройте Large Object
        cursor.execute(sql.SQL("SELECT lo_close(%s)"), (image_file,))

        # Вставьте запись о Large Object в таблицу
        cursor.execute("INSERT INTO pictures (name, pic_oid, owner_id, password) VALUES (%s, %s, %s, %s)",
                       (name, image_oid, str(user_id), password))

        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

# Функция, которая будет выполняться для каждого активного бота
def start_bot(token):
    bot_instance = telebot.TeleBot(token)

    @bot_instance.message_handler(commands=['start'])
    def handle_start(message):
        print('Received /start command')
        user_id = message.from_user.id
        reg_date = datetime.now().date()

        # Проверка, существует ли пользователь в БД
        db_cursor.execute("SELECT * FROM telegram_user WHERE telegram_id = %s", (str(user_id),))
        existing_user = db_cursor.fetchone()

        if existing_user is not None:
            # Обновить last_login для существующего пользователя
            update_last_login(user_id)
        else:
            # Добавить нового пользователя в БД
            db_cursor.execute("INSERT INTO telegram_user (telegram_id, reg_date, last_login) VALUES (%s, %s, %s)",
                            (str(user_id), reg_date, reg_date))  # Здесь last_login устанавливается как текущая дата

        datebase.commit()

        bot_instance.send_message(user_id, "Добро пожаловать! Вы зарегистрированы в системе.")

    @bot_instance.message_handler(commands=['sendimage'])
    def handle_sendimage(message):
        user_id = message.from_user.id
        bot_instance.send_message(user_id, "Введите имя для изображения:")
        bot_instance.register_next_step_handler(message, process_image_name)

    def process_image_name(message):
        user_id = message.from_user.id
        image_name = message.text
        bot_instance.send_message(user_id, "Нужен ли пароль для изображения? (Да/Нет)")
        bot_instance.register_next_step_handler(message, process_password, user_id, image_name)

    def process_password(message, user_id, image_name):
        password_needed = message.text.lower()
        if password_needed == "да":
            bot_instance.send_message(user_id, "Введите пароль для изображения:")
            bot_instance.register_next_step_handler(message, process_image_password, user_id, image_name)
        elif password_needed == "нет":
            bot_instance.send_message(user_id, "Отправьте изображение:")
            bot_instance.register_next_step_handler(message, process_image_data, user_id, image_name, None)
        else:
            bot_instance.send_message(user_id, "Пожалуйста, ответьте 'Да' или 'Нет'.")

    def process_image_password(message, user_id, image_name):
        image_password = message.text
        bot_instance.send_message(user_id, "Отправьте изображение:")
        bot_instance.register_next_step_handler(message, process_image_data, user_id, image_name, image_password)

    def process_image_data(message, user_id, image_name, image_password):
        if message.photo:
            file_info = bot_instance.get_file(message.photo[0].file_id)
            file_path = file_info.file_path
            image_data = bot_instance.download_file(file_path)

            # Сохраните изображение в базе данных с использованием Large Objects
            save_image(user_id, image_name, image_password, image_data)
            bot_instance.send_message(user_id, "Изображение сохранено в базе данных.")
        else:
            bot_instance.send_message(user_id, "Пожалуйста, отправьте изображение.")

    bot_instance.remove_webhook()
    bot_instance.polling(none_stop=True)
