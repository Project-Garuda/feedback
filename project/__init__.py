from flask import Flask, render_template, request, redirect, url_for, Blueprint, flash
from sqlalchemy.orm import scoped_session, sessionmaker
app = Flask(__name__, static_url_path='/static')

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
app.register_blueprint(mod_student, url_prefix='/student')
@app.route("/", methods=['GET', 'POST'])
def home():
    if request.form:
        print('DataPassed through post')
        print(request.form)
        return redirect(url_for('.student.student_dashboard'))
    return render_template('index.html')

@app.route("/check_post/",methods=['GET','POST'])
def check_post():
    print("Data passed through post")
    return render_template('index.html')
