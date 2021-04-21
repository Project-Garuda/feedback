from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import scoped_session, sessionmaker
import pymysql

from project import Base

"""Consists of all the Classes related to student"""
"""All the passwords are hashed and stored in the database using flask bcrypt"""

class Student(Base):
    """Student Credentials are stored in this class."""
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    name =  Column(String(50))
    section = relationship('UploadSection', backref = 'upload_section')
    password = Column(String(255), nullable=False)
    filled = relationship('Filled', backref='filled')

    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password

class Section(Base):
    """Class which contais all the section ID's"""
    __tablename__ = 'section'
    id = Column(String(10),primary_key = True)

    def __init__(self,id):
        self.id = id

class UploadSection(Base):
    """Class which consists of list of students in each section.Each feild has a student id and ID which specifies a student belongs to a particular section"""
    __tablename__ = 'upload_section'
    sno = Column(Integer , primary_key = True)
    id = Column(String(10), ForeignKey('section.id', onupdate='CASCADE', ondelete='CASCADE'))
    student_id = Column(Integer, ForeignKey('student.id', onupdate='CASCADE', ondelete='CASCADE'))

    def __init__(self, id, student_id):
        self.id = id
        self.student_id = student_id
