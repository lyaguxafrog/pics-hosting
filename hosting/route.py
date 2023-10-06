# -*- coding: utf-8 -*-


from hosting import app

@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'
