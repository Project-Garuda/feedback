from unittest import mock
from flask_testing import TestCase
from project import  bcrypt, app, delete_engine_models, db_session, create_engine_models
from project.mod_faculty.models import Faculty,Courses , Feedback, Theory, Lab, Tutorial, UploadCourses, Admin
from project.mod_student.models import Student, UploadSection, Section
global init_database
init_database = False
class BaseTestCase(TestCase):
    def create_app(self):
        """
        Create an instance of the app with the testing configuration
        :return:
        """
        from project import app, DATABASE_URI
        app.config['feedback_status'] = 1
        app.config['TESTING'] = True
        return app

    def setUp(self):
        self.app.preprocess_request()
        global init_database
        if init_database is False:
            init_database = True
            db_session.add(Student(1801083,'Shravan',  bcrypt.generate_password_hash('1801083').decode('utf-8')))
            db_session.add(Faculty(2801083,'Shravan',  bcrypt.generate_password_hash('2801083').decode('utf-8')))
            db_session.add(Admin(3801081,'Shravan',  bcrypt.generate_password_hash('testing').decode('utf-8')))
            db_session.add(Courses('CS351', 'IT Workshop III: Cloud Computing'))
            db_session.add(Courses('CS350', 'Software Engineering'))
            db_session.add(Courses('CS331', 'Software Engineering Lab'))
            db_session.add(Courses('CS101', 'Computer Programming'))
            db_session.add(Section('CG31'))
            db_session.add(UploadSection('CG31',1801083))
            db_session.commit()
            db_session.add(UploadCourses('CS350', 'CG31', 2801083, 0))
            db_session.commit()
            db_session.add(UploadCourses('CS331', 'CG31', 2801083, 1))
            db_session.commit()
            db_session.add(UploadCourses('CS101', 'CG31', 2801083, 2))
            db_session.commit()
            db_session.add(Theory(1))
            db_session.add(Lab(2))
            db_session.add(Tutorial(3))
            db_session.commit()
