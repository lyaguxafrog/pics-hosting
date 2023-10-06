# -*- coding: utf-8 -*- 

from flask import Flask

from flask_sqlalchemy import SQLAlchemy

import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


app = Flask(__name__)

db_path = os.getenv("DATABASE")
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}' 
db = SQLAlchemy(app)


from hosting import admin, route
