# -*- coding: utf-8 -*-

from flask_admin.contrib.sqla import ModelView

from hosting.services.db import db

class Bot(db.Model):
    """ Класс описывающий бота """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    bot_token = db.Column(db.String)
    comment = db.Column(db.Text)
    is_active = db.Column(db.Boolean)


class BotAdmin(ModelView):
    """ Класс описывающий поведение Bot в админке """
    column_list = ('id', 'name', 'bot_token', 'comment', 'is_active')
    column_searchable_list = ('id', 'name')
    column_filters = ('is_active',)
    form_columns = ('id', 'name', 'bot_token', 'comment', 'is_active')
