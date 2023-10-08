# -*- coding: utf-8 -*-

from werkzeug.security import generate_password_hash

from hosting import db, app
from hosting.models import Admins

app.app_context().push()

username = input("username: ")
password = input("password: ")
password_hash = generate_password_hash(password)


user = Admins(username=username, password=password_hash) 
db.session.add(user)
db.session.commit()
print(f"User {username} created successfully!")

db.create_all()
