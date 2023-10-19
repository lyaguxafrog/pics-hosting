# -*- coding: utf-8 -*-


from datetime import datetime


from bot.services.db_connection import db

con = db()
cur = con.cursor()


def last_login_update(telegram_id: str) -> None:
    """
    Функция апдейта last_login

    :param telegram_id: ID пользователя

    :return: None
    """

    last_login = datetime.now().date()

    cur.execute(f"UPDATE telegram_user SET last_login = %s WHERE telegram_id = %s", (last_login, telegram_id))
