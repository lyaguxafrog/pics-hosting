# -*- coding: utf-8 -*-

from hosting import db, app
from hosting.models import Bot



def tokens() -> list:
    with app.app_context():
        """
        Функция получения токенов из БД 

        :return: list всех токенов
        """

        tokens = Bot.query.with_entities(Bot.bot_token).filter(Bot.is_active == True).all()
        token_list = [token[0] for token in tokens]
        
        return token_list
