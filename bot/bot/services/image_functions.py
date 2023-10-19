# -*- coding: utf-8 -*-

from bot.services.dbconnect import db


def get_user_images(user_id):
    conn = db()  # Подключение к базе данных
    cursor = conn.cursor()

    # Определяем SQL-запрос для извлечения изображений пользователя
    select_query = "SELECT * FROM pictures WHERE owner_id = %s"
    cursor.execute(select_query, (str(user_id),))  # Преобразуйте user_id в строку
    user_images = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]

    # Закрываем соединение
    cursor.close()
    conn.close()

    return user_images
