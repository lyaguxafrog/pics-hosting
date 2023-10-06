# -*- coding: utf-8 -*- 


from flask_admin.contrib.sqla import ModelView
from flask_security import UserMixin


from hosting import db


class User(db.Model, UserMixin):
    """ Класс описывающий пользователя, нужен для доступа в админ-панель """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean(), default=True)


class UserAdmin(ModelView):
    """ Класс описывающий поведение User в админ панели  """
    column_list = ('id', 'username', 'email', 'password', 'active')
    column_searchable_list = ('id', 'username', 'email')
    column_filters = ('id', 'email', 'active')
    form_columns = ('id', 'username', 'email', 'password', 'active')
