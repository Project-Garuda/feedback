from project.mod_student.models import Student
from project import db_session
from flask import Flask, render_template, request, redirect, url_for, Blueprint, session

mod_student = Blueprint('student', __name__)


@mod_student.route("/", methods=['GET', 'POST'])
def student_dashboard():
    if 'user' in session:
        print(session['user'])
        return "student_dashboard"
    else:
        return 'Please login'
