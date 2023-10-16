# -*- coding: utf-8 -*-

from flask import request

from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

from werkzeug.security import check_password_hash, generate_password_hash
import pyotp

from hosting import db

class Admins(db.Model, UserMixin):
    """" Класс описывающий админ-юзера """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_2FA = db.Column(db.Boolean)
    otp_secret = db.Column(db.String(16))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def generate_otp_secret(self):
        self.otp_secret = pyotp.random_base32()

    def verify_otp(self, otp, username):
        totp = pyotp.TOTP(self.otp_secret)
        return totp.verify(otp, username)

class AdminsAdmin(ModelView):
    """ Класс описывающий поведение Bot в админке """

    column_list = ('id', 'username', 'is_2FA')
    column_searchable_list = ('id', 'username')
    column_filters = ('username',)
    form_columns = ('username', 'password', 'is_2FA')
