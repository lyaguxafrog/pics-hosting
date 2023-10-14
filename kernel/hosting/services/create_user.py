# -*- coding: utf-8 -*-

from werkzeug.security import generate_password_hash

from hosting import db, app
from hosting.models import Admins

app.app_context().push()

username = input("username: ")
password = input("password: ")
password_hash = generate_password_hash(password)

try:
    opt_ch = int(input("Генерация OTP:\n1 - Сгенерировать OTP и включить 2FA\n2 - не генерировать\n: "))

    if opt_ch == 1:
        opt = True

        user = Admins(username=username, password=password_hash, is_2FA=opt)
        user.generate_otp_secret()
        print(f"User {username} created successfully!")


    elif opt_ch == 2:
        opt = False

        user = Admins(username=username, password=password_hash, is_2FA=opt)
        print(f"User {username} created successfully!")


except:
    exit()


db.session.add(user)
db.session.commit()

db.create_all()
