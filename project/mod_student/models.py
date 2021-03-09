from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import pymysql

from project import Base
class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    name =  Column(String(50))

    def __init__(self, name):
        self.name = name
