# -*- coding: utf-8 -*-

from flask import redirect

from hosting import app

@app.route('/')
def index():
    return redirect('/admin')
