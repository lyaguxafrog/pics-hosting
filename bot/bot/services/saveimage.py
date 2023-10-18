
from bot.services.dbconnect import db

datebase = db()
db_cursor = datebase.cursor()

def save_image(user_id, name, password, pic_data):
    try:
        # Начать новую транзакцию
        datebase.commit()

        # Вставить данные изображения в таблицу
        db_cursor.execute("INSERT INTO pictures (name, pic_data, owner_id, password) VALUES (%s, %s, %s::character varying, %s::character varying)", (name, pic_data, str(user_id), password))

        # Завершить транзакцию
        datebase.commit()
    except Exception as e:
        # Если произошла ошибка, откатить транзакцию
        datebase.rollback()
        print(f"Error: {e}")
