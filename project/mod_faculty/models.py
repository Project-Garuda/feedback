from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import scoped_session, sessionmaker
import pymysql

from project import Base
from project.mod_student.models import Student, Section

class Faculty(Base):
    __tablename__ = 'faculty'
    id = Column(Integer, primary_key=True)
    name =  Column(String(50))
    courses = relationship('UploadCourses', backref='faculty')
    password = Column(String(255), nullable=False)

    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password

class Admin(Base):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True)
    name =  Column(String(50))
    password = Column(String(255), nullable=False)

    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password

class Courses(Base):
    __tablename__ = 'courses'
    id = Column(String(10), primary_key=True)
    name =  Column(String(100))

    def __init__(self,id, name):
        self.id = id
        self.name = name

class UploadCourses(Base):
    """docstring for UploadCourses.
        0 for course , 1 for lab, 2 for tutorial
    """
    __tablename__ = 'upload_courses'
    id = Column(Integer, primary_key=True)
    course_id = Column(String(10), ForeignKey('courses.id', onupdate='CASCADE', ondelete='CASCADE'))
    section_id = Column(String(10), ForeignKey('section.id', onupdate='CASCADE', ondelete='CASCADE'))
    faculty_id = Column(Integer, ForeignKey('faculty.id', onupdate='CASCADE', ondelete='CASCADE'))
    course = Column(Integer, default = 0)

    def __init__(self, course_id, section_id, faculty_id, course):
        self.course_id = course_id
        self.section_id = section_id
        self.faculty_id = faculty_id
        self.course = course

class Feedback(Base):
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True)
    upload_courses_id = Column(Integer, ForeignKey('upload_courses.id', onupdate='CASCADE', ondelete='CASCADE'))
    remark = Column(Text())

    def __init__(self, upload_courses_id, remark):
        self.upload_courses_id = upload_courses_id
        self.remark = remark

class Filled(Base):
    __tablename__ = 'filled'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('student.id', onupdate='CASCADE', ondelete='CASCADE'))
    upload_courses_id = Column(Integer, ForeignKey('upload_courses.id', onupdate='CASCADE', ondelete='CASCADE'))

    def __init__(self, student_id, upload_courses_id):
        self.student_id = student_id
        self.upload_courses_id = upload_courses_id

class Theory(Base):
    __tablename__ = 'theory'
    id = Column(Integer, ForeignKey('upload_courses.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    no_respones = Column(Integer, default = 0)
    p1 = Column(Float, default = 5)
    p2 = Column(Float, default = 5)
    p3 = Column(Float, default = 5)
    p4 = Column(Float, default = 5)
    p5 = Column(Float, default = 5)
    p6 = Column(Float, default = 5)
    p7 = Column(Float, default = 5)
    p8 = Column(Float, default = 5)
    p9 = Column(Float, default = 5)
    p10 = Column(Float, default = 5)
    p11 = Column(Float, default = 5)
    p12 = Column(Float, default = 5)
    p13 = Column(Float, default = 5)
    p14 = Column(Float, default = 5)
    p15 = Column(Float, default = 5)

    def __init__(self, id):
        self.id = id

    def fetch_dict(self):
        return {
                'p1':self.p1 ,
                'p2':self.p2 ,
                'p3':self.p3 ,
                'p4':self.p4 ,
                'p5':self.p5 ,
                'p6':self.p6 ,
                'p7':self.p7 ,
                'p8':self.p8 ,
                'p9':self.p9 ,
                'p10':self.p10 ,
                'p11':self.p11 ,
                'p12':self.p12 ,
                'p13':self.p13 ,
                'p14':self.p14 ,
                'p15':self.p15
        }

class Lab(Base):
    __tablename__ = 'lab'
    id = Column(Integer, ForeignKey('upload_courses.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    no_respones = Column(Integer, default = 0)
    p1 = Column(Float, default = 5)
    p2 = Column(Float, default = 5)
    p3 = Column(Float, default = 5)
    p4 = Column(Float, default = 5)
    p5 = Column(Float, default = 5)
    p6 = Column(Float, default = 5)
    p7 = Column(Float, default = 5)
    p8 = Column(Float, default = 5)
    p9 = Column(Float, default = 5)
    p10 = Column(Float, default = 5)

    def __init__(self, id):
        self.id = id

    def fetch_dict(self):
        return {
                'p1':self.p1 ,
                'p2':self.p2 ,
                'p3':self.p3 ,
                'p4':self.p4 ,
                'p5':self.p5 ,
                'p6':self.p6 ,
                'p7':self.p7 ,
                'p8':self.p8 ,
                'p9':self.p9 ,
                'p10':self.p10
        }

class Tutorial(Base):
    __tablename__ = 'tutorial'
    id = Column(Integer, ForeignKey('upload_courses.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    no_respones = Column(Integer, default = 0)
    p1 = Column(Float, default = 5)
    p2 = Column(Float, default = 5)
    p3 = Column(Float, default = 5)
    p4 = Column(Float, default = 5)
    p5 = Column(Float, default = 5)
    p6 = Column(Float, default = 5)
    p7 = Column(Float, default = 5)
    p8 = Column(Float, default = 5)

    def __init__(self, id):
        self.id = id

    def fetch_dict(self):
        return {
                'p1':self.p1 ,
                'p2':self.p2 ,
                'p3':self.p3 ,
                'p4':self.p4 ,
                'p5':self.p5 ,
                'p6':self.p6 ,
                'p7':self.p7 ,
                'p8':self.p8
        }
