# -*- coding: utf-8 -*-

from werkzeug.security import generate_password_hash

from hosting import db, app
from hosting.models import Admins


import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


dbname = os.getenv("POSTGRES_DB")
password = os.getenv("POSTGRES_PASSWORD")
user = os.getenv("POSTGRES_USER")

app.app_context().push()


username = "admin"
password = "admin"
password_hash = generate_password_hash(password)


user = Admins(username=username, password=password_hash, is_2FA=False)


db.session.add(user)
db.session.commit()

db.create_all()
