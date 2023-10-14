# -*- coding: utf-8 -*-


from flask import (render_template,
            redirect, url_for, flash, request, redirect, send_file)

from flask_login import login_user, login_required, logout_user, current_user

from hosting import app
from hosting.models import Admins, Pictures

import io

@app.route('/')
def index():
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Admins.query.filter_by(username=username).first()

        if user and user.check_password(password): 
            login_user(user)
            return redirect(url_for('admin.index'))
        else:
            flash('Неправильное имя пользователя или пароль', 'error')

    return render_template('login.html')


@app.route('/logout')
@login_required 
def logout():
    logout_user()  
    flash('Вы успешно вышли из системы.', 'success') 
    return redirect(url_for('login')) 


@app.route('/view-image/<int:id>/', methods=['GET'])
def view_image(id):
    picture = Pictures.query.get(id)
    if picture:
        response = send_file(
            io.BytesIO(picture.pic_data),
            mimetype='image/jpg',  # Замените на соответствующий MIME-тип
            as_attachment=False  # Изменено с as_attachment=True
        )
        return response
    return "Image not found", 404
