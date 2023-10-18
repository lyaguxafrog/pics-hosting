# -*- coding: utf-8 -*-

from flask import Flask

from flask_bootstrap import Bootstrap

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())



app = Flask(__name__)
bootstrap = Bootstrap(app)


app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

login_manager = LoginManager(app)


POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")



app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:5432/{POSTGRES_DB}'
db = SQLAlchemy(app)



from hosting import admin, route
