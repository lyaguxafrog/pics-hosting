# -*- coding: utf-8 -*- 

from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


app = Flask(__name__)


app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

login_manager = LoginManager(app)


db_path = os.getenv("DATABASE")
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}' 
db = SQLAlchemy(app)


from hosting.bot_kernel import bot
from hosting import admin, route
