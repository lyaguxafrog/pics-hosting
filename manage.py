#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from hosting.services.logs import logging

from hosting import app
from hosting import db

import time
import os
import sys

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


if len(sys.argv) > 1 and sys.argv[1] == 'sql':
    import hosting.services.sql_tools

else:
    if __name__ == '__main__':
        with app.app_context():
            db.create_all()
            app.run(debug=os.getenv("DEBUG"))
