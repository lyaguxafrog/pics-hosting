# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Column, Integer, LargeBinary, String, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2


Base = declarative_base()
