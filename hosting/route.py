# -*- coding: utf-8 -*-


from flask import render_template, redirect, url_for, flash, request, redirect

from flask_login import login_user, login_required, logout_user, current_user

from hosting import app
from hosting.models import Admins

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
