# -*- coding: utf-8 -*-


from datetime import datetime

from bot.services.dbconnect import db


datebase = db()
db_cursor = datebase.cursor()


def update_last_login(user_id):
    last_login = datetime.now().date()

    try:
        # Начать новую транзакцию
        datebase.commit()

        # Выполнить запрос на обновление last_login
        db_cursor.execute("UPDATE telegram_user SET last_login = %s WHERE telegram_id = %s::character varying", (last_login, str(user_id)))

        # Завершить транзакцию
        datebase.commit()
    except Exception as e:
        # Если произошла ошибка, откатить транзакцию
        datebase.rollback()
        print(f"Error: {e}")
