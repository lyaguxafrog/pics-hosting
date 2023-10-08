# -*- coding: utf-8 -*-

from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

from werkzeug.security import check_password_hash, generate_password_hash

from hosting import db

class Admins(db.Model, UserMixin):
    """" Класс описывающий админ-юзера """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class AdminsAdmin(ModelView):
    """ Класс описывающий поведение Bot в админке """

    column_list = ('id', 'username', 'password')
    column_searchable_list = ('id', 'username')
    column_filters = ('username',)
    form_columns = ('id', 'username', 'password')
