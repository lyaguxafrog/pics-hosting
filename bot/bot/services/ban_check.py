# -*- coding: utf-8 -*-


from bot.services.db_connection import db


con = db()
cur = con.cursor()


def check_ban(user_id: str) -> bool:
    """
    Функция проверки на бан

    :param user_id: ID пользователя

    :return: True - бан / False - не бан
    """

    cur.execute("SELECT is_banned FROM telegram_user WHERE telegram_id = %s", (user_id,))
    result = cur.fetchone()


    if result is not None and result[0] is True:
        return True
    else:
        return False
