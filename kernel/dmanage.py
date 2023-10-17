#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request

from hosting import app
from hosting import db

import os
import sys
import time
import threading

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())



if len(sys.argv) > 1 and sys.argv[1] == 'sql':
    import hosting.services.sql_tools

elif len(sys.argv) > 1 and sys.argv[1] == 'su':
    import hosting.services.create_user

elif len(sys.argv) > 1 and sys.argv[1] == 'sa':
    import hosting.services.add_admin


else:
    if __name__ == '__main__':
        with app.app_context():
            db.create_all()
            app.run(debug=os.getenv("DEBUG"), host='0.0.0.0', port=8080)
