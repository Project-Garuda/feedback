from project.mod_faculty.models import Faculty
from project import db_session, bcrypt
from flask import Flask, render_template, request, redirect, url_for, Blueprint, session

mod_faculty = Blueprint('faculty', __name__)

@mod_faculty.route("/", methods=['GET', 'POST'])
def faculty_dashboard():
    if 'user' in session:
        return render_template('faculty_dashboard.html')
    else:
        return redirect(url_for('home'))
