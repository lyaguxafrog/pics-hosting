# -*- codimg: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy

import os
from dotenv import load_dotenv, find_dotenv

from hosting import app

load_dotenv(find_dotenv())

db_path = os.getenv("DATABASE")
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}' 
db = SQLAlchemy(app)
