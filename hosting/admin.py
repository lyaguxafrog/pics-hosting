# -*- coding: utf-8 -*-

from flask import Flask

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

import os
from dotenv import load_dotenv, find_dotenv

from hosting import app
from hosting.models.db import db

from hosting.models import User, UserAdmin

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")


admin = Admin(app)
admin.add_view(UserAdmin(User, db.session))


