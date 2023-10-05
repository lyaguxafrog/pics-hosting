# -*- coding: utf-8 -*-
# app/services/sql_tools.py

import sqlite3 as sql

import time

from app.services.logs import logs_gen


logs_gen(logs_type="I", logs_message="Start option 'sql'")

try:
    db = str(input("DB: "))
    logs_gen(logs_type='I', logs_message=f'Connect to {db}')
except:
    exit()

print(f'Connect: {db}')

db_path = f'app/db/{db}'

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
