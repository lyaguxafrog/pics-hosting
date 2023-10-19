
from datetime import datetime

from bot.services.db_connection import db
from bot.services.ban_check import check_ban


def handler_start(message, bot):
    """ Обработчик команды /start """

    conn = db()
    cur = conn.cursor()

    telegram_id = str(message.from_user.id)
    reg_date = datetime.now().date()

    cur.execute("SELECT telegram_id FROM telegram_user WHERE telegram_id = %s", (telegram_id,))
    existing_user = cur.fetchone()

    if existing_user is None:

        cur.execute("INSERT INTO telegram_user (telegram_id, reg_date, last_login) VALUES (%s, %s, %s)",
                    (telegram_id, reg_date, reg_date))

        bot.send_message(telegram_id, f"Добро пожаловать! Вы зарегистрированы в системе.\nВаш ID: {telegram_id}\nДата регистрации: {reg_date}")
        bot.send_message(telegram_id, "Команды:\n/help - это сообщение\n/new_image - отправить сообщение\n/my_images - мои сообщения")

    else:

        if check_ban(user_id=telegram_id):

            bot.send_message(telegram_id, "У Вас нет доступа.")

        else:

            cur.execute(f"UPDATE telehram_user (last_login) WHERE telegram_id='{telegram_id}' VALUES ({reg_date})")
            bot.send_message(telegram_id, "Команды:\n/help - это сообщение\n/new_image - отправить сообщение\n/my_images - мои сообщения")


    conn.commit()
