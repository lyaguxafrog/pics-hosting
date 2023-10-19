
import telebot
import psycopg2
from PIL import Image
import io
import os
from multiprocessing import Process
from datetime import datetime
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.services.get_tokens import get_active_bot_tokens
from bot.services.dbconnect import db
from bot.services.last_login import update_last_login
from bot.services.saveimage import save_image

# Функция для получения списка активных токенов из базы данных
tokens = get_active_bot_tokens(db_connection=db())

datebase = db()
db_cursor = datebase.cursor()

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
        bot_instance.send_message(user_id, "Отправьте изображение в виде файла (или /cancel для отмены):")
        bot_instance.register_next_step_handler(message, process_image_data, user_id)

    def process_image_data(message, user_id):
        if message.text and message.text.lower() == "/cancel":
            bot_instance.send_message(user_id, "Отправка изображения отменена.")
            return
        elif message.photo:
            bot_instance.send_message(user_id, "Пожалуйста, отправьте изображение в виде файла.")
        elif message.document:
            # Обработка прикрепленного документа (файла)
            file_info = bot_instance.get_file(message.document.file_id)
            file_path = file_info.file_path

            bot_instance.send_message(user_id, "Введите имя для изображения:")
            bot_instance.register_next_step_handler(message, process_image_name, user_id, file_path)
        else:
            bot_instance.send_message(user_id, "Пожалуйста, отправьте изображение в виде файла.")

    def process_image_name(message, user_id, file_path):
        image_name = message.text
        bot_instance.send_message(user_id, "Нужен ли пароль для изображения? (Да/Нет)")
        bot_instance.register_next_step_handler(message, process_password, user_id, file_path, image_name)

    def process_password(message, user_id, file_path, image_name):
        password_needed = message.text.lower()
        if password_needed == "да":
            bot_instance.send_message(user_id, "Введите пароль для изображения:")
            bot_instance.register_next_step_handler(message, process_image_password, user_id, file_path, image_name)
        elif password_needed == "нет":
            save_image_to_database(user_id, image_name, file_path, None)
            bot_instance.send_message(user_id, "Изображение сохранено в базе данных.")
        else:
            bot_instance.send_message(user_id, "Пожалуйста, ответьте 'Да' или 'Нет'.")

    def process_image_password(message, user_id, file_path, image_name):
        image_password = message.text
        save_image_to_database(user_id, image_name, file_path, image_password)
        bot_instance.send_message(user_id, "Изображение сохранено в базе данных.")


    def save_image_to_database(user_id, image_name, file_path, image_password):
        conn = db()

        cursor = conn.cursor()

        # Определяем SQL-запрос для вставки данных об изображении
        insert_query = """
            INSERT INTO pictures (name, pic_data, file_path, owner_id, password, is_one_view, view)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        # Выполняем SQL-запрос
        cursor.execute(insert_query, (image_name, None, file_path, user_id, image_password, False, 0))

        # Фиксируем изменения
        conn.commit()

        # Закрываем соединение
        cursor.close()
        conn.close()


    @bot_instance.message_handler(commands=['cancel'])
    def handle_cancel(message):
        user_id = message.from_user.id
        bot_instance.send_message(user_id, "Отправка изображения отменена.")




    bot_instance.remove_webhook()
    bot_instance.polling(none_stop=True)
