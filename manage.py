#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hosting.services.logs import logging

from hosting import app

import time
import os
import sys

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

if __name__ == '__main__':
    try:
        if len(sys.argv) > 1 and sys.argv[1] == 'sql':
            import hosting.services.sql_tools
        else:
            pass
    
    except KeyboardInterrupt:
        time.sleep(1)
        exit()

else:
    if __name__ == '__main__':
        app.run(debug=os.getenv("DEBUG"))
