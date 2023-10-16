# -*- codingL utf-8 -*-


from sqlalchemy import create_engine, Column, Integer, LargeBinary, String, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2


from bot import Base


class TelegramUser(Base):
    """ Класс описывающий пользователя """

    __tablename__ = 'telegram_user'
    telegram_id = Column(Integer, primary_key=True)
    reg_date = Column(DateTime)
    last_login = Column(DateTime)
    is_prem = Column(Boolean,default=False)
    pics_count = Column(Integer)
    is_banned = Column(Boolean, default=False)
    comment = Column(Text)
