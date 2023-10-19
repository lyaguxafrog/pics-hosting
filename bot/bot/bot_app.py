
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
from bot.services.image_functions import get_user_images

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
            save_image(user_id, image_name, file_path, None)  # Сохраняем изображение в папку
            save_image_to_database(user_id, image_name, file_path, None)  # Сохраняем информацию в базу данных
            bot_instance.send_message(user_id, "Изображение сохранено в папку и базу данных.")
        else:
            bot_instance.send_message(user_id, "Пожалуйста, ответьте 'Да' или 'Нет'.")

    def process_image_password(message, user_id, file_path, image_name):
        image_password = message.text
        save_image(user_id, image_name, file_path, image_password)  # Сохраняем изображение в папку
        save_image_to_database(user_id, image_name, file_path, image_password)  # Сохраняем информацию в базу данных
        bot_instance.send_message(user_id, "Изображение сохранено в папку и базу данных.")



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



    @bot_instance.message_handler(commands=['viewimages'])
    def handle_viewimages(message):
        user_id = message.from_user.id
        user_images = get_user_images(user_id)  # Получите список изображений пользователя из базы данных (предположим, что у вас есть функция для этого)

        if not user_images:
            bot_instance.send_message(user_id, "У вас пока нет добавленных изображений.")
            return

        markup = InlineKeyboardMarkup(row_width=1)

        for image in user_images:
            button = InlineKeyboardButton(image['name'], callback_data=f"view_image_{image['id']}")
            markup.add(button)

        bot_instance.send_message(user_id, "Выберите изображение для просмотра:", reply_markup=markup)

    @bot_instance.callback_query_handler(func=lambda call: call.data.startswith('view_image_'))
    def view_image_callback(call):
        user_id = call.from_user.id
        image_id = int(call.data.split('_')[-1])

        image_data = get_image_data(image_id)  # Получите данные изображения по image_id из базы данных

        if not image_data:
            bot_instance.answer_callback_query(call.id, "Изображение не найдено.")
            return

        # Откройте файл изображения из папки imgs/ и отправьте его как фото
        image_path = os.path.join("imgs", f"{user_id}_{image_data['name']}.jpg")

        with open(image_path, "rb") as image_file:
            bot_instance.send_photo(user_id, image_file, caption=image_data['name'])

        # Создайте клавиатуру для управления изображением (изменения имени, пароля и т. д.)
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("Изменить имя", callback_data=f"edit_name_{image_id}"),
            InlineKeyboardButton("Включить пароль", callback_data=f"enable_password_{image_id}"),
            InlineKeyboardButton("Сменить пароль", callback_data=f"change_password_{image_id}"),
            InlineKeyboardButton("Изменить параметры просмотра", callback_data=f"edit_view_settings_{image_id}")
        )

        # Отправьте клавиатуру управления
        bot_instance.send_message(user_id, "Выберите действие:", reply_markup=markup)


    @bot_instance.callback_query_handler(func=lambda call: call.data.startswith('edit_name_'))
    def edit_name_callback(call):
        user_id = call.from_user.id
        image_id = int(call.data.split('_')[-1])

        bot_instance.send_message(user_id, "Введите новое имя для изображения:")

        # Регистрируйте обработчик для получения нового имени
        bot_instance.register_next_step_handler(call.message, process_new_name, user_id, image_id)

    @bot_instance.callback_query_handler(func=lambda call: call.data.startswith('enable_password_'))
    def enable_password_callback(call):
        user_id = call.from_user.id
        image_id = int(call.data.split('_')[-1])

        bot_instance.send_message(user_id, "Введите новый пароль для изображения:")

        # Регистрируйте обработчик для включения пароля
        bot_instance.register_next_step_handler(call.message, process_enable_password, user_id, image_id)

    @bot_instance.callback_query_handler(func=lambda call: call.data.startswith('edit_name_'))
    def edit_name_callback(call):
        user_id = call.from_user.id
        image_id = int(call.data.split('_')[-1])  # Исправленная строка

        bot_instance.send_message(user_id, "Введите новое имя для изображения:")

        # Регистрируйте обработчик для получения нового имени
        bot_instance.register_next_step_handler(call.message, process_new_name, user_id, image_id)

    @bot_instance.callback_query_handler(func=lambda call: call.data.startswith('enable_password_'))
    def enable_password_callback(call):
        user_id = call.from_user.id
        image_id = int(call.data.split('_')[-1])  # Исправленная строка

        bot_instance.send_message(user_id, "Введите новый пароль для изображения:")

        # Регистрируйте обработчик для включения пароля
        bot_instance.register_next_step_handler(call.message, process_enable_password, user_id, image_id)

    @bot_instance.callback_query_handler(func=lambda call: call.data.startswith('change_password_'))
    def change_password_callback(call):
        user_id = call.from_user.id
        image_id = int(call.data.split('_')[-1])  # Исправленная строка

        bot_instance.send_message(user_id, "Введите новый пароль для изображения:")

        # Регистрируйте обработчик для смены пароля
        bot_instance.register_next_step_handler(call.message, process_change_password, user_id, image_id)

    @bot_instance.callback_query_handler(func=lambda call: call.data.startswith('edit_view_settings_'))
    def edit_view_settings_callback(call):
        user_id = call.from_user.id
        image_id = int(call.data.split('_')[-1])  # Исправленная строка

        # Здесь предоставьте опции для изменения параметров просмотра (например, в один просмотр)
        # Регистрируйте обработчик для изменения параметров просмотра
        bot_instance.send_message(user_id, "Выберите параметры просмотра:", reply_markup=your_custom_markup)

        bot_instance.register_next_step_handler(call.message, process_edit_view_settings, user_id, image_id)


    def process_new_name(message, user_id, image_id):
        new_name = message.text

        # Обновите имя изображения в базе данных по image_id
        update_image_name(image_id, new_name)

        bot_instance.send_message(user_id, "Имя изображения обновлено успешно.")

    def process_enable_password(message, user_id, image_id):
        # Включите пароль для изображения в базе данных по image_id
        enable_image_password(image_id)

        bot_instance.send_message(user_id, "Пароль включен для изображения.")

    def process_change_password(message, user_id, image_id):
        new_password = message.text

        # Измените пароль изображения в базе данных по image_id
        change_image_password(image_id, new_password)

        bot_instance.send_message(user_id, "Пароль изображения изменен успешно.")


    bot_instance.remove_webhook()
    bot_instance.polling(none_stop=True)
