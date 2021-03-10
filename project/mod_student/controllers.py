from project.mod_student.models import Student
from project import db_session as db
stu = Student(1801081, 'shravan')
db.add(stu)
db.commit()
