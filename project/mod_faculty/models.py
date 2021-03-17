from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
import pymysql

from project import Base
from project.mod_student.models import Student, Section

class Faculty(Base):
    __tablename__ = 'faculty'
    id = Column(Integer, primary_key=True)
    name =  Column(String(50))
    password = Column(String(255),nullable=False)
    courses = relationship('UploadCourses',backref='faculty')
    feedback = relationship('Feedback', backref='faculty')

    def __init__(self, name):
        self.id = id
        self.name = name

class Courses(Base):
    __tablename__ = 'courses'
    id = Column(String(10),primary_key=True)
    name = Column(String(100))

    def __init__(self,id,name):
        self.id = id
        self.name = name

class UploadCourses(Base):
    __tablename__ = 'upload_courses'
    id = Column(Integer,primary_key=True)
    rating = Column(Integer,default=5)
    section_id = Column(String(10),ForeignKey('section.id',onupdate='CASCADE',ondelete='CASCADE'))
    faculty_id = Column(Integer,ForeignKey('faculty.id',onupdate='CASCADE',ondelete='CASCADE'))
    course_id  = Column(String(10),ForeignKey('courses.id',onupdate='CASCADE',ondelete='CASCADE'))
    no_responses = Column(Integer,default=0)
    type = Column(Integer,default=0) #0=theory,1=lab,2=tutorial

    def __init__(self,rating,section_id,faculty_id,course_id,no_responses,type):
        self.rating = rating
        self.section_id = section_id
        self.faculty_id = faculty_id
        self.course_id = course_id
        self.no_responses = no_responses
        self.type = type

class Feedback(Base):
    __tablename__ = 'feedback'
    id = Column(Integer,primary_key=True)
    section_id = Column(String(10),ForeignKey('section.id',onupdate='CASCADE',ondelete='CASCADE'))
    faculty_id = Column(Integer,ForeignKey('faculty.id',onupdate='CASCADE',ondelete='CASCADE'))
    course_id  = Column(String(10),ForeignKey('courses.id',onupdate='CASCADE',ondelete='CASCADE'))
    remark = Column(Text())

    def __init__(self, section_id, faculty_id,course_id,remarks):
        self.section_id = section_id
        self.faculty_id = faculty_id
        self.course_id = course_id
        self.remark = remark

class Filled(Base):
    __tablename__ = 'filled'
    id = Column(Integer,primary_key=True)
    student_id = Column(Integer,ForeignKey('student.id',onupdate='CASCADE',ondelete='CASCADE'))
    upload_courses_id = Column(Integer,ForeignKey('upload_courses.id',onupdate='CASCADE',ondelete='CASCADE'))

    def __init__(self, student_id,upload_courses_id):
        self.student_id = student_id
        self.upload_courses_id = upload_courses_id
