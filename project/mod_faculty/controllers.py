from project.mod_faculty.models import Faculty,Courses , Feedback, Theory, Lab, Tutorial, UploadCourses, Admin
from project import db_session, bcrypt, app
from flask import Flask, render_template, request, redirect, url_for, Blueprint, session , abort, flash
from project.mod_student.models import Section

mod_faculty = Blueprint('faculty', __name__)

@mod_faculty.route("/" ,methods=['GET', 'POST'])
def faculty_dashboard():
    if 'faculty' in session:
        faculty = Faculty.query.filter(Faculty.id == session['faculty']).first()
        print(faculty)
        return render_template('faculty/faculty_dashboard.html',
        faculty = faculty,
        session = session,
        course_names = Courses,
        )
    else:
        return redirect(url_for('home'))

@mod_faculty.route('/logout')
def logout():
    if 'faculty' in session:
        session.pop('faculty', None)
        return redirect(url_for('home'))
    return redirect(url_for('home'))

@mod_faculty.route('/create', methods=['GET', 'POST'])
def create_course():
    if 'faculty' in session:
        faculty = Faculty.query.filter(Faculty.id == session['faculty']).first()
        if request.method == "POST":
            print('Hello')
            course_id = request.form['course_id'].upper()
            section_id = request.form['section_id'].upper()
            dict = {'Theory':0, 'Lab':1, 'Tutorial':2}
            type = dict[request.form['type']]
            course = Courses.query.filter(Courses.id == course_id).first()
            section = Courses.query.filter(Section.id == section_id).first()
            print(type)
            if course is None:
                flash('Invalid Course ID')
                return redirect(url_for('.create_course'))
            if section is None:
                flash('Invalid Section ID')
                return redirect(url_for('.create_course'))
            try:
                check = UploadCourses.query.filter(
                            UploadCourses.course_id == course_id,
                            UploadCourses.section_id == section_id,
                            UploadCourses.faculty_id == faculty.id,
                            UploadCourses.course == type
                        ).first()
                if check is not None:
                    flash('Course already exists')
                    return redirect(url_for('.create_course'))
                my_obj = UploadCourses(course_id, section_id, faculty.id, type)
                db_session.add(my_obj)
                db_session.commit()
                if type == 0:
                    db_session.add(Theory(my_obj.id))
                elif type == 1:
                    db_session.add(Lab(my_obj.id))
                else:
                    db_session.add(Tutorial(my_obj.id))
                db_session.commit()
                flash('Course created Successfully')
                return redirect(url_for('.faculty_dashboard'))
            except Exception as e:
                print(e)
                flash('Unknown error')
                return redirect(url_for('.faculty_dashboard'))

        return render_template('faculty/create_course.html',
        faculty = faculty,
        session = session,
        )

@mod_faculty.route('/view/<int:id>', methods=['GET'])
def view_responses(id):
    if 'faculty' in session:
        faculty = Faculty.query.filter(Faculty.id == session['faculty']).first()
        my_obj = UploadCourses.query.filter(UploadCourses.id == id).first()
        if my_obj.course == 0:
            theory = Theory.query.filter(Theory.id == id).first()
            if theory is None:
                abort(404)
            theory_dict = theory.fetch_dict()
            theory_dict['no_respones'] = theory.no_respones
            remarks = Feedback.query.with_entities(Feedback.remark).filter(my_obj.id == Feedback.upload_courses_id).all()
            print(remarks)
            return render_template('faculty/view_responses_theory.html',
            faculty = faculty,
            dict = theory_dict,
            remarks = remarks
            )
        elif my_obj.course == 1:
            lab = Lab.query.filter(Lab.id == id).first()
            print(lab)
            if lab is None:
                abort(404)
            lab_dict = lab.fetch_dict()
            lab_dict['no_respones'] = lab.no_respones
            remarks = Feedback.query.with_entities(Feedback.remark).filter(my_obj.id == Feedback.upload_courses_id).all()
            print(remarks)
            return render_template('faculty/view_responses_lab.html',
            faculty = faculty,
            dict = lab_dict,
            remarks = remarks
            )
        else:
            tutorial = Tutorial.query.filter(Tutorial.id == id).first()
            if tutorial is None:
                abort(404)
            tutorial_dict = tutorial.fetch_dict()
            tutorial_dict['no_respones'] = tutorial.no_respones
            remarks = Feedback.query.with_entities(Feedback.remark).filter(my_obj.id == Feedback.upload_courses_id).all()
            print(remarks)
            return render_template('faculty/view_responses_tutorial.html',
            faculty = faculty,
            dict = tutorial_dict,
            remarks = remarks
            )
    else:
        return redirect(url_for('home'))
