from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import scoped_session, sessionmaker
import pymysql

from project import Base

class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    name =  Column(String(50))
    section = relationship('UploadSection', backref = 'upload_section')

    def __init__(self, id, name):
        self.id = id
        self.name = name

class Section(Base):
    """docstring for Section."""
    __tablename__ = 'section'
    id = Column(String(10),primary_key = True)

    def __init__(self,id):
        self.id = id

class UploadSection(Base):
    """docstring for Section."""
    __tablename__ = 'upload_section'
    sno = Column(Integer , primary_key = True)
    id = Column(String(10), ForeignKey('section.id', onupdate='CASCADE', ondelete='CASCADE'))
    student_id = Column(Integer, ForeignKey('student.id', onupdate='CASCADE', ondelete='CASCADE'))

    def __init__(self, id, student_id):
        self.id = id
        self.student_id = student_id
