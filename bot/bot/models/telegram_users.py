from sqlalchemy import Column, String, Date, Boolean, Integer, Text, LargeBinary
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TelegramUser(Base):
    __tablename__ = 'telegram_user'
    telegram_id = Column(String, primary_key=True)
    reg_date = Column(Date)
    last_login = Column(Date)
    is_prem = Column(Boolean, default=False)
    pics_count = Column(Integer)
    is_banned = Column(Boolean, default=False)
    comment = Column(Text)
