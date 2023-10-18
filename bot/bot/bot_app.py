
import telebot
import psycopg2
from PIL import Image
import io
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

            # Сохранить изображение в базе данных
            image_data = io.BytesIO(image_data)
            image = Image.open(image_data)
            image_format = "PNG"  # Используем формат PNG
            image.save(image_data, format=image_format)

            image_data.seek(0)  # Сбросить указатель потока

            # Сохранить изображение в базе данных
            save_image(user_id, image_name, image_password, image_data.read())
            bot_instance.send_message(user_id, "Изображение сохранено в базе данных.")
        else:
            bot_instance.send_message(user_id, "Пожалуйста, отправьте изображение.")




    @bot_instance.message_handler(commands=['viewimages'])
    def handle_viewimages(message):
        user_id = message.from_user.id
        db_cursor.execute("SELECT id, name FROM pictures WHERE owner_id = %s", (str(user_id),))
        saved_images = db_cursor.fetchall()

        if saved_images:
            markup = InlineKeyboardMarkup(row_width=2)

            for image_id, image_name in saved_images:
                button = InlineKeyboardButton(image_name, callback_data=f"view_{image_id}")
                markup.add(button)

            bot_instance.send_message(user_id, "Выберите изображение для просмотра:", reply_markup=markup)
        else:
            bot_instance.send_message(user_id, "У вас нет сохраненных изображений.")

    @bot_instance.callback_query_handler(func=lambda call: call.data.startswith("view_"))
    def callback_view_image(call):
        user_id = call.from_user.id
        image_id = call.data.split("_")[1]

        db_cursor.execute("SELECT pic_data FROM pictures WHERE id = %s AND owner_id = %s", (image_id, str(user_id)))
        image_data = db_cursor.fetchone()

        if image_data:
            bot_instance.send_photo(user_id, image_data[0])
        else:
            bot_instance.send_message(user_id, "Изображение не найдено.")

    bot_instance.remove_webhook()
    bot_instance.polling(none_stop=True)
