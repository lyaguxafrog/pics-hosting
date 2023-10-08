# -*- coding: utf-8 -*-


from hosting import db, app
from hosting.models import Admins

app.app_context().push()

username = input("username: ")
password = input("password: ")


user = Admins(username=username, password=password) 
db.session.add(user)
db.session.commit()
print(f"User {username} created successfully!")

db.create_all()
