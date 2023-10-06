# -*- coding: utf-8 -*-

from flask_admin.contrib.sqla import ModelView

from hosting import db

class TelegramUser(db.Model):
    """ Класс описывающий пользователя """
    telegram_id = db.Column(db.Integer, primary_key=True)
    reg_date = db.Column(db.Date)
    last_login = db.Column(db.Date)
    is_prem = db.Column(db.Boolean)
    pics_count = db.Column(db.Integer)
    is_banned = db.Column(db.Boolean)
    comment = db.Column(db.Text)


class TelegramUserAdmin(ModelView):
    """ Класс описывающий поведение TelegramUser в админке """
    column_list = ('telegram_id', 'is_prem', 'reg_date', 'pics_count', 'last_login', 'comment')
    column_searchable_list = ('telegram_id',) 
    column_filters = ('is_prem',)
    form_columns = ('telegram_id', 'is_prem', 'reg_date', 'pics_count', 'last_login', 'comment')
