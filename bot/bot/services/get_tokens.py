# -*- coding: utf-8 -*-


def get_active_bot_tokens(db_connection):
    """
    Функция получения активных ботов

    :param db_connection: подключение БД
    :return: Токены ботов
    """
    cursor = db_connection.cursor()
    cursor.execute("SELECT bot_token FROM bot WHERE is_active = true;")
    tokens = {row[0] for row in cursor.fetchall()}
    cursor.close()
    return tokens
