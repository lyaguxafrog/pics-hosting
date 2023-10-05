# -*- coding: utf-8 -*-
# app/services/logs.py

import logging
import datetime

now = str(datetime.datetime.now())
logging.basicConfig(level=logging.INFO, filename=f"{now}.log",filemode="w",
                     format="%(asctime)s %(levelname)s %(message)s")

def logs_gen(logs_type: str, logs_message: str) -> None:
    """
    Функция логирования 
    
    :param logs_type: Тип логирования: I -> INFO, W -> WARNING, E -> ERROR, C -> CRITICAL
    :param logs_message: Сообщение в логи

    :returns: None
    """


    if logs_type == 'I':
        logging.info(msg=logs_message)
    elif logs_type == 'W':
        logging.warning(msg=logs_message)
    elif logs_type == 'E':
        logging.error(msg=logs_message)
    elif logs_type == 'C':
        logging.critical(msg=logs_message)
    else:
        logging.warning(msg='Не верный тип логгирования')
