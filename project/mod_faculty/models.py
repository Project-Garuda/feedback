from sqlalchemy import Column, Integer, String, ForeignKey, Text
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
    feedback = relationship('Feedback', backref='faculty')

    def __init__(self, name):
        self.name = name

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
    rating = Column(Integer, default = 5)
    course_id = Column(String(10), ForeignKey('courses.id', onupdate='CASCADE', ondelete='CASCADE'))
    section_id = Column(String(10), ForeignKey('section.id', onupdate='CASCADE', ondelete='CASCADE'))
    faculty_id = Column(Integer, ForeignKey('faculty.id', onupdate='CASCADE', ondelete='CASCADE'))
    no_respones = Column(Integer, default = 0)
    course = Column(Integer, default = 0)

    def __init__(self, rating, course_id, section_id, faculty_id, no_respones, course):
        self.rating = rating
        self.course_id = course_id
        self.section_id = section_id
        self.faculty_id = faculty_id
        self.no_respones = no_respones
        self.course = course


class Feedback(Base):
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True)
    course_id = Column(String(10), ForeignKey('courses.id', onupdate='CASCADE', ondelete='CASCADE'))
    section_id = Column(String(10), ForeignKey('section.id', onupdate='CASCADE', ondelete='CASCADE'))
    faculty_id = Column(Integer, ForeignKey('faculty.id', onupdate='CASCADE', ondelete='CASCADE'))
    remark = Column(Text())

    def __init__(self, course_id, name, faculty_id, remark):
        self.name = name
        self.course_id = remark
        self.faculty_id = faculty_id
        self.remark = remark

class Filled(Base):
    __tablename__ = 'filled'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('student.id', onupdate='CASCADE', ondelete='CASCADE'))
    upload_courses_id = Column(Integer, ForeignKey('upload_courses.id', onupdate='CASCADE', ondelete='CASCADE'))

    def __init__(self, student_id, upload_courses_id):
        self.student_id = student_id
        self.upload_courses_id = upload_courses_id
