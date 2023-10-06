# -*- coding: utf-8 -*-

from flask import Flask

from flask_admin import Admin

import os
from dotenv import load_dotenv, find_dotenv

import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from hosting import app
from hosting import db

from hosting.models import (TelegramUser, TelegramUserAdmin, Bot, BotAdmin, User, UserAdmin)


# security = Security(app)
# login_manager = LoginManager(app)


app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")


admin = Admin(app)
admin.add_view(TelegramUserAdmin(TelegramUser, db.session))
admin.add_view(BotAdmin(Bot, db.session))
admin.add_view(UserAdmin(User, db.session))


