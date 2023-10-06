# -*- coding: utf-8 -*-

from flask import Flask

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from hosting import app
from hosting.services.db import db

from hosting.models import User, UserAdmin, Bot, BotAdmin

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")


admin = Admin(app)
admin.add_view(UserAdmin(User, db.session))
admin.add_view(BotAdmin(Bot, db.session))


