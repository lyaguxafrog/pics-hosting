# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Date, Boolean, Integer, Text, LargeBinary
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Picture(Base):
    __tablename__ = 'pictures'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    pic_data = Column(LargeBinary)
    file_path = Column(String)
    owner_id = Column(String)
    password = Column(String)
    is_one_view = Column(Boolean)
    view = Column(Integer, default=0)
