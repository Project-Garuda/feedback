from flask import Flask, render_template, request, redirect, url_for, Blueprint, flash, session
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import and_, func
from flask_bcrypt import Bcrypt

app = Flask(__name__, static_url_path='/static', template_folder='templates')
app.secret_key = 'Helloworld'
UPLOAD_FOLDER = '/home/shravan/SE/project/static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['feedback_status'] = 0
bcrypt = Bcrypt(app)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()
DATABASE_URI = 'sqlite:///:memory:' #This is for testing
#DATABASE_URI = 'mysql+pymysql://shravan:kvshravan1@@localhost:3306/college'
try:
    engine = create_engine(DATABASE_URI, echo = False)
except Exception as e:
    print(e)
db_session = scoped_session(sessionmaker(bind=engine))
Base.query = db_session.query_property()

def create_engine_models():
    Base.metadata.create_all(engine)

from project.mod_student import models
from project.mod_faculty import models
create_engine_models()
def delete_engine_models():
    db_session.close_all()
    Base.metadata.drop_all(engine)

from project.mod_student import controllers
from project.mod_student.controllers import mod_student
from project.mod_student.models import Student
from project.mod_faculty import controllers
from project.mod_faculty.controllers import mod_faculty
from project.mod_admin import controllers
from project.mod_admin.controllers import mod_admin
from project.mod_faculty.models import Faculty , Theory, Admin
app.register_blueprint(mod_student, url_prefix='/student')
app.register_blueprint(mod_faculty, url_prefix='/faculty')
app.register_blueprint(mod_admin, url_prefix='/admin')


@app.route("/", methods=['GET', 'POST'])
def home():
    if 'student' in session:
        return redirect(url_for('.student.student_dashboard'))
    if 'faculty' in session:
        return redirect(url_for('.faculty.faculty_dashboard'))
    if request.method == "POST":
        user_id = request.form['login_username']
        if request.form['role'] == 'student':
            if app.config['feedback_status'] == 0:
                flash('Currently system is not accepting any feedbacks.')
                return redirect(url_for('home'))
            student = Student.query.filter(Student.id == user_id).first()
            if student and bcrypt.check_password_hash(student.password, request.form['secretkey']):
                session['student'] = user_id
                return redirect(url_for('.student.student_dashboard'))
            else:
                flash("Login failed!")
        if request.form['role'] == 'faculty':
            faculty = Faculty.query.filter(Faculty.id == user_id).first()
            if faculty and bcrypt.check_password_hash(faculty.password, request.form['secretkey']):
                session['faculty'] = user_id
                return redirect(url_for('.faculty.faculty_dashboard'))
            else:
                flash("Login failed!")

    return render_template('index.html')

@app.route("/admin", methods=['GET', 'POST'])
def admin_home():
    if 'admin' in session:
        return redirect(url_for('.admin.admin_dashboard'))
    if request.method == "POST":
        user_id = request.form['login_username']
        admin = Admin.query.filter(Admin.id == user_id).first()
        if admin and bcrypt.check_password_hash(admin.password, request.form['secretkey']):
            session['admin'] = user_id
            return redirect(url_for('.admin.admin_dashboard'))
        else:
            flash("Login failed!")

    return render_template('admin_index.html')

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
