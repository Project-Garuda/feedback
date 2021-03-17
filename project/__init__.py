from flask import Flask, render_template, request, redirect, url_for, Blueprint, flash, session
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import and_, func
from flask_bcrypt import Bcrypt

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'Helloworld'
bcrypt = Bcrypt(app)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()
DATABASE_URI = 'mysql+pymysql://shravan:kvshravan1@@localhost:3306/college'
engine = create_engine(DATABASE_URI,echo = True)
db_session = scoped_session(sessionmaker(bind=engine))
Base.query = db_session.query_property()

def create_engine_models():
    Base.metadata.create_all(engine)

from project.mod_student import models
from project.mod_faculty import models
create_engine_models()

from project.mod_student import controllers
from project.mod_student.controllers import mod_student
from project.mod_student.models import Student
app.register_blueprint(mod_student, url_prefix='/student')


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        user_id = request.form['login_username']
        if request.form['role'] == 'student':
            student = Student.query.filter(Student.id == user_id).first()
            print(student.password)
            print(request.form['secretkey'])
            print(bcrypt.check_password_hash(student.password, request.form['secretkey']))
            if student and bcrypt.check_password_hash(student.password, request.form['secretkey']):
                return redirect(url_for('.student.student_dashboard'))
            else:
                return " Login unsuccessful"
    return render_template('index.html')
