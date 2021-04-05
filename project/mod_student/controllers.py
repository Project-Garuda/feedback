from project.mod_student.models import Student
from project.mod_faculty.models import UploadCourses, Courses, Faculty, Filled, Theory, Feedback, Lab, Tutorial
from project import db_session, bcrypt, app
from sqlalchemy import and_, func
from flask import Flask, render_template, request, redirect, url_for, Blueprint, session, abort, jsonify, flash
from sqlalchemy.orm import load_only

mod_student = Blueprint('student', __name__)

@mod_student.route("/" ,methods=['GET', 'POST'])
def student_dashboard():
    if app.config['feedback_status'] == 0:
        flash('Currently system is not accepting any feedbacks.')
        logout()
    if 'student' in session:
        student = Student.query.filter(Student.id == session['student']).first()
        print(student)
        section_ids = []
        for section in student.section:
            section_ids.append(section.id)
        upload_courses = UploadCourses.query.filter(UploadCourses.section_id.in_(section_ids)).all()
        return render_template('student/student_dashboard.html',
        student = student,
        upload_courses = upload_courses,
        course_names = Courses,
        faculty = Faculty,
        filled = Filled
        )
    else:
        return redirect(url_for('home'))
@mod_student.route('/logout')
def logout():
    if 'student' in session:
        session.pop('student', None)
        return redirect(url_for('home'))
    return redirect(url_for('home'))

@mod_student.route('/submit/<int:id>',methods=['GET', 'POST'])
def submit_feedback(id):
    if 'student' in session:
        if request.method == "POST":
            print('Hello')
            print(request.form)
            my_obj = UploadCourses.query.filter(UploadCourses.id == id).first()
            if my_obj.course == 0:
                theory = Theory.query.filter(Theory.id == id).first()
                if theory is None:
                    abort(404)
                theory_dict = theory.fetch_dict()
                for elem in theory_dict:
                    theory_dict[elem] = (theory.no_respones*theory_dict[elem]+int(request.form[elem]))/(theory.no_respones+1)
                theory_dict['id'] = id
                theory_dict['no_respones'] = theory.no_respones+1
                update_theory = Theory.query.filter(Theory.id == id).update(theory_dict)
            elif my_obj.course == 1:
                lab = Lab.query.filter(Lab.id == id).first()
                if lab is None:
                    abort(404)
                lab_dict = lab.fetch_dict()
                for elem in lab_dict:
                    lab_dict[elem] = (lab.no_respones*lab_dict[elem]+int(request.form[elem]))/(lab.no_respones+1)
                lab_dict['id'] = id
                lab_dict['no_respones'] = lab.no_respones+1
                update_lab = Lab.query.filter(Lab.id == id).update(lab_dict)
            else:
                tutorial = Tutorial.query.filter(Tutorial.id == id).first()
                if tutorial is None:
                    abort(404)
                tutorial_dict = tutorial.fetch_dict()
                for elem in tutorial_dict:
                    tutorial_dict[elem] = (tutorial.no_respones*tutorial_dict[elem]+int(request.form[elem]))/(tutorial.no_respones+1)
                tutorial_dict['id'] = id
                tutorial_dict['no_respones'] = tutorial.no_respones+1
                update_tutorial = Tutorial.query.filter(Tutorial.id == id).update(tutorial_dict)

            filled = Filled(session['student'], id)
            db_session.add(filled)
            remark = request.form['remark'].strip()
            if len(remark) > 0:
                print(remark)
                db_session.add(Feedback(id,remark))

            try:
                db_session.commit()
                flash('Feedback Submitted Successfully.')
            except Exception as e:
                print(e)
            return redirect(url_for('.student_dashboard'))
        else:
            student = Student.query.filter(Student.id == session['student']).first()
            section_ids = []
            for section in student.section:
                section_ids.append(section.id)
            student_courses = UploadCourses.query.with_entities(UploadCourses.id).filter(UploadCourses.section_id.in_(section_ids)).all()
            not_present = True
            for course in student_courses:
                print(course)
                if id == course[0]:
                    print(course[0])
                    not_present = False
                    break
            if not_present:
                abort(404)
            if Filled.query.filter(Filled.student_id == student.id, Filled.upload_courses_id == id).first() is not None:
                abort(404)
            current_upload_course_obj = UploadCourses.query.filter(UploadCourses.id == id).first()
            faculty_name = Faculty.query.with_entities(Faculty.name).filter(Faculty.id == current_upload_course_obj.faculty_id).first()
            course_name = Courses.query.with_entities(Courses.name).filter(Courses.id == current_upload_course_obj.course_id).first()
            print(faculty_name, course_name)
            if current_upload_course_obj.course == 0:
                return render_template('student/theory_form.html',
                    student = student,
                    upload_courses_id = current_upload_course_obj.id,
                    course_id = current_upload_course_obj.course_id,
                    course_name = course_name[0],
                    faculty_name = faculty_name[0]
                 )
            elif current_upload_course_obj.course == 1:
                return render_template('student/lab_form.html',
                    upload_courses_id = current_upload_course_obj.id,
                    course_id = current_upload_course_obj.course_id,
                    course_name = course_name[0],
                    faculty_name = faculty_name[0]
                 )
            else:
                return render_template('student/tutorial_form.html',
                    upload_courses_id = current_upload_course_obj.id,
                    course_id = current_upload_course_obj.course_id,
                    course_name = course_name[0],
                    faculty_name = faculty_name[0]
                 )
    else:
        return redirect(url_for('home'))

@mod_student.route('/change',methods=['GET', 'POST'])
def change_password():
    if 'student' in session:
        student = Student.query.filter(Student.id == session['student']).first()
        if request.method == "POST":
            if bcrypt.check_password_hash(student.password, request.form['old_pass']):
                new_pass = bcrypt.generate_password_hash(request.form['new_pass']).decode('utf-8')
                update_student = Student.query.filter(Student.id == session['student']).update({'password': new_pass})
                try:
                    db_session.commit()
                    flash('Successfully Updated Password')
                    return redirect(url_for('.student_dashboard'))
                except Exception as e:
                    print(e)
                    flash('Unknown error!')
                    return redirect(url_for('.change_password'))
            else:
                flash('Old Password is incorrect')
                return redirect(url_for('.change_password'))
        return render_template('student/change_password.html',
        student = student,
        session = session,
        )
    else:
        return redirect(url_for('home'))
