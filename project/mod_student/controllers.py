from project.mod_student.models import Student
from project import db_session, app
from flask import Flask, render_template, request, redirect, url_for, Blueprint

mod_student = Blueprint('student', __name__)


@mod_student.route("/", methods=['GET', 'POST'])
def student_dashboard():
    return "student_dashboard"
