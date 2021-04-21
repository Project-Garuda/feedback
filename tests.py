from project import app
import unittest
from flask import url_for, request
from base import BaseTestCase
from project.mod_faculty.models import Faculty,Courses , Feedback, Theory, Lab, Tutorial, UploadCourses, Admin

class TestLogin(BaseTestCase):

    def test_student_login(self):
        with self.app.test_client() as c:
            response = c.post('/', data=dict(login_username = '1801083', secretkey= '1801083', role = 'student'))
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, url_for('student.student_dashboard', _external=True))

    def test_faculty_login(self):
        with self.app.test_client() as c:
            response = c.post('/', data=dict(login_username = '2801083', secretkey= '2801083', role = 'faculty'))
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, url_for('faculty.faculty_dashboard', _external=True))

    def test_admin_login(self):
        with self.app.test_client() as c:
            response = c.post('/admin', data=dict(login_username = '3801081', secretkey= 'testing'))
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, url_for('admin.admin_dashboard', _external=True))

    def test_invalid_faculty_login(self):
        with self.app.test_client() as c:
            response = c.post('/', data=dict(login_username = '380', secretkey= '2801083', role = 'faculty'))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Login failed!", response.data)

    def test_invalid_student_login(self):
        with self.app.test_client() as c:
            response = c.post('/', data=dict(login_username = '380', secretkey= '2801083', role = 'student'))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Login failed!", response.data)

    def test_invalid_admin_login(self):
        with self.app.test_client() as c:
            response = c.post('/admin', data=dict(login_username = '380', secretkey= '2801083'))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Login failed!", response.data)

class TestLogOut(BaseTestCase):

    def test_if_logout_redirects_to_login_student(self):
        with self.app.test_client() as c:
            response = c.post('/', data=dict(login_username = '1801083', secretkey= '1801083', role = 'student'))
            self.assertEqual(response.status_code, 302)
            response = c.get(url_for('student.logout'), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"You have been logged out", response.data)
            self.assert_template_used('index.html')

    def test_if_logout_redirects_to_login_faculty(self):
        with self.app.test_client() as c:
            response = c.post('/', data=dict(login_username = '2801083', secretkey= '2801083', role = 'faculty'))
            self.assertEqual(response.status_code, 302)
            response = c.get(url_for('faculty.logout'), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"You have been logged out", response.data)
            self.assert_template_used('index.html')

    def test_if_logout_redirects_to_login_admin(self):
        with self.app.test_client() as c:
            response = c.post('/admin', data=dict(login_username = '3801081', secretkey= 'testing'))
            self.assertEqual(response.status_code, 302)
            response = c.get(url_for('admin.logout'), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"You have been logged out", response.data)
            self.assert_template_used('admin_index.html')


class TestFacultyControllers(BaseTestCase):

    def test_create_course(self):
        with self.app.test_client() as c:
            response = c.post('/', data=dict(login_username = '2801083', secretkey= '2801083', role = 'faculty'))
            self.assertEqual(response.status_code, 302)
            response = c.post('/faculty/create', data=dict(course_id = 'CS351', section_id = 'CG31', type = 'Theory'), follow_redirects = True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Course created Successfully", response.data)
            self.assert_template_used('faculty/faculty_dashboard.html')
            check = UploadCourses.query.filter(
                        UploadCourses.course_id == 'CS351',
                        UploadCourses.section_id == 'CG31',
                        UploadCourses.faculty_id == '2801083',
                        UploadCourses.course == 0
                    ).first()
            theory = Theory.query.filter(check.id == Theory.id).first()
            self.assertNotEqual(check, None)
            self.assertNotEqual(theory, None)

    def test_create_course_invalid_course(self):
        with self.app.test_client() as c:
            response = c.post('/', data=dict(login_username = '2801083', secretkey= '2801083', role = 'faculty'))
            self.assertEqual(response.status_code, 302)
            response = c.post('/faculty/create', data=dict(course_id = 'CS352', section_id = 'CG31', type = 'Theory'), follow_redirects = True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Invalid Course ID", response.data)
            self.assert_template_used('faculty/create_course.html')
            check = UploadCourses.query.filter(
                        UploadCourses.course_id == 'CS352',
                        UploadCourses.section_id == 'CG31',
                        UploadCourses.faculty_id == '2801083',
                        UploadCourses.course == 0
                    ).first()
            self.assertEqual(check, None)

    def test_create_course_invalid_section(self):
        with self.app.test_client() as c:
            response = c.post('/', data=dict(login_username = '2801083', secretkey= '2801083', role = 'faculty'))
            self.assertEqual(response.status_code, 302)
            response = c.post('/faculty/create', data=dict(course_id = 'CS351', section_id = 'CG32', type = 'Theory'), follow_redirects = True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Invalid Section ID", response.data)
            self.assert_template_used('faculty/create_course.html')
            check = UploadCourses.query.filter(
                        UploadCourses.course_id == 'CS352',
                        UploadCourses.section_id == 'CG32',
                        UploadCourses.faculty_id == '2801083',
                        UploadCourses.course == 0
                    ).first()
            self.assertEqual(check, None)

    def test_create_course_already_existing_course(self):
        with self.app.test_client() as c:
            response = c.post('/', data=dict(login_username = '2801083', secretkey= '2801083', role = 'faculty'))
            self.assertEqual(response.status_code, 302)
            response = c.post('/faculty/create', data=dict(course_id = 'CS350', section_id = 'CG31', type = 'Theory'), follow_redirects = True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Course already exists", response.data)
            self.assert_template_used('faculty/create_course.html')
            check = UploadCourses.query.filter(
                        UploadCourses.course_id == 'CS350',
                        UploadCourses.section_id == 'CG31',
                        UploadCourses.faculty_id == '2801083',
                        UploadCourses.course == 0
                    ).count()
            self.assertEqual(check, 1)

    def test_view_responses_invalid_id(self):
        with self.app.test_client() as c:
            response = c.post('/', data=dict(login_username = '2801083', secretkey= '2801083', role = 'faculty'))
            self.assertEqual(response.status_code, 302)
            response = c.get('/faculty/view/69420')
            self.assertEqual(response.status_code, 404)

    def test_view_responses_theory(self):
        with self.app.test_client() as c:
            response = c.post('/', data=dict(login_username = '2801083', secretkey= '2801083', role = 'faculty'))
            self.assertEqual(response.status_code, 302)
            response = c.get('/faculty/view/1',  follow_redirects = True)
            self.assertEqual(response.status_code, 200)
            self.assert_template_used('faculty/view_responses_theory.html')

    def test_view_responses_lab(self):
        with self.app.test_client() as c:
            response = c.post('/', data=dict(login_username = '2801083', secretkey= '2801083', role = 'faculty'))
            self.assertEqual(response.status_code, 302)
            response = c.get('/faculty/view/2',  follow_redirects = True)
            self.assertEqual(response.status_code, 200)
            self.assert_template_used('faculty/view_responses_lab.html')

    def test_view_responses_tutorial(self):
        with self.app.test_client() as c:
            response = c.post('/', data=dict(login_username = '2801083', secretkey= '2801083', role = 'faculty'))
            self.assertEqual(response.status_code, 302)
            response = c.get('/faculty/view/3',  follow_redirects = True)
            self.assertEqual(response.status_code, 200)
            self.assert_template_used('faculty/view_responses_tutorial.html')

    def test_delete_course(self):
        with self.app.test_client() as c:
            response = c.post('/', data=dict(login_username = '2801083', secretkey= '2801083', role = 'faculty'))
            self.assertEqual(response.status_code, 302)
            response = c.get('/faculty/delete/4', follow_redirects = True)
            self.assert_template_used('faculty/faculty_dashboard.html')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Course deleted Successfully", response.data)

    def test_change_password_faculty(self):
       with self.app.test_client() as c:
           response = c.post('/', data=dict(login_username = '2801083', secretkey= '2801083', role = 'faculty'),follow_redirects=True)
           self.assertEqual(response.status_code, 200)
           response = c.post('/faculty/change', data=dict(old_pass = '2801083', new_pass = '2801084'),follow_redirects=True)
           self.assertEqual(response.status_code, 200)
           self.assertIn(b"Successfully Updated Password",response.data)
           response = c.get(url_for('faculty.logout'), follow_redirects=True)
           self.assertEqual(response.status_code, 200)
           self.assertIn(b"You have been logged out", response.data)
           response = c.post('/', data=dict(login_username = '2801083', secretkey= '2801084', role = 'faculty'))
           self.assertEqual(response.status_code, 302)
           self.assertEqual(response.location, url_for('faculty.faculty_dashboard', _external=True))
           response = c.post('/faculty/change', data=dict(old_pass = '2801084', new_pass = '2801083'))
           self.assertEqual(response.status_code, 302)
           self.assertEqual(response.location, url_for('faculty.faculty_dashboard', _external=True))
           response = c.get(url_for('faculty.logout'), follow_redirects=True)
           self.assertEqual(response.status_code, 200)
           self.assertIn(b"You have been logged out", response.data)


class TestInvalidAccess(BaseTestCase):
    def test_invalid_access_faculty(self):
        with self.app.test_client() as c:
            response = c.get('/faculty',  follow_redirects = True)
            self.assert_template_used('index.html')
            response = c.get('/faculty/logout',  follow_redirects = True)
            self.assert_template_used('index.html')
            response = c.get('/faculty/view/1',  follow_redirects = True)
            self.assert_template_used('index.html')
            response = c.get('/faculty/create',  follow_redirects = True)
            self.assert_template_used('index.html')
            response = c.get('/faculty/change',  follow_redirects = True)
            self.assert_template_used('index.html')
            response = c.get('/faculty/delete',  follow_redirects = True)
            self.assert_template_used('index.html')

    def test_invalid_access_student(self):
        with self.app.test_client() as c:
            response = c.get('/student',  follow_redirects = True)
            self.assert_template_used('index.html')
            response = c.get('/student/logout',  follow_redirects = True)
            self.assert_template_used('index.html')
            response = c.get('/student/submit/1',  follow_redirects = True)
            self.assert_template_used('index.html')
            response = c.get('/student/change',  follow_redirects = True)
            self.assert_template_used('index.html')

if __name__ == '__main__':
    unittest.main()
