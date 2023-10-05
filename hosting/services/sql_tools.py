# -*- coding: utf-8 -*-
# app/services/sql_tools.py

import sqlite3 as sql

import time

from hosting.services.logs import logs_gen

'''
Инструмент управления БД.
Вызывается "./manage.py sql"

Нужен для редактирования и создания БД без развертывания приложений
'''


logs_gen(logs_type="I", logs_message="Start option 'sql'") # запись в логи

try:
    db = str(input("DB: ")) # подключение к бд
    logs_gen(logs_type='I', logs_message=f'Connect to {db}')
except:
    exit()

print(f'Connect: {db}')

db_path = f'hosting/db/{db}'

try:
    while True:
        con = sql.connect(str(db_path), check_same_thread=False)
        cur = con.cursor()

        query = str(input("SQL: "))
        cur.execute(query)
        print(f'>{query}')

except KeyboardInterrupt:
    time.sleep(1)
    con.close()
    print('\nClosed...')
    exit()
