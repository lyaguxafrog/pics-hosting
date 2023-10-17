from flask import request
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, StringField
from wtforms.validators import InputRequired
from werkzeug.security import check_password_hash, generate_password_hash
import pyotp

from hosting import db

class Admins(db.Model, UserMixin):
    """ Класс описывающий админ-юзера """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_2FA = db.Column(db.Boolean, default=False)
    otp_secret = db.Column(db.String(64))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def generate_otp_secret(self):
        self.otp_secret = pyotp.random_base32()

    def verify_otp(self, otp):
        if self.is_2FA and self.otp_secret:
            totp = pyotp.TOTP(self.otp_secret)
            return totp.verify(otp)
        return False

class AdminForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    is_2FA = BooleanField('Enable 2FA')
    otp_secret = StringField('OTP Secret')

class AdminsAdmin(ModelView):
    """ Класс описывающий поведение Admins в админке """

    column_list = ('id', 'username', 'is_2FA')
    column_searchable_list = ('id', 'username')
    column_filters = ('username', 'is_2FA')
    form_columns = ('username', 'password', 'is_2FA', 'otp_secret')

    form = AdminForm  # Используйте созданную форму

    def on_model_change(self, form, model, is_created):
        if 'password' in form:
            if form.password.data:
                model.password = generate_password_hash(form.password.data)

        if 'is_2FA' in form:
            model.is_2FA = form.is_2FA.data
            if form.is_2FA.data:
                model.generate_otp_secret()
            else:
                model.otp_secret = None  # Удалите OTP-секрет, если 2FA отключена

    def create_form(self):
        form = super(AdminsAdmin, self).create_form()
        form.otp_secret.data = pyotp.random_base32()
        return form
