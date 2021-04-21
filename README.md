# Faculty Feedback Management System
It is a feedback system where students give their feedback on their corresponding faculties over a semester. These reviews are retrieved and average calculations are performed.These ratings and reviews are displayed to admin authorities to investigate the faculty performance, which will, in turn, helps them to smoothen the teaching-learning process.Student anonymity will be maintained.

## Installation
### Fetch requirements
```
pip3 -r requirements.txt
```
### Run Flask server
```
python3 run.py
```
## PURPOSE 
  The purpose of developing this “Faculty Feedback Management System” is to make the process of Faculty
Feedback simple and easier by avoiding manual feedback system.

## SCOPE
  It will integrate the benefits of a feedback with the convenience of a ‘no manual’ feedback collection. This will
provide more flexibility in getting the feedback without any manual distribution of feedback forms among the
students. The system is more secure and reliable in terms of feedback cause the system ensures that a student cannot
fill a form more than once and only registered students can fill the form.

## Proposed System
  The new feedback management system makes the process easier. The proposed system has three interfaces
one for faculty, one for admin and one for students. Admin needs to enter the details of courses taken by each
student, the section he/she is enrolled in and the details of the course instructors. Student needs to open the portal
and select course from the list of courses available and submit the feedback. Faculty can login and view the
responses submitted for their respective courses. 

#### The system has been presented with the following interfaces :)

### Admin :
![Admin_Dashboard](https://user-images.githubusercontent.com/47289942/115505495-2e91ca80-a297-11eb-8c43-38cb0f2e43fe.png)
* Upload Data: Admin uploads the credentials of faculty,student.Along with the credentials admin needs to upload the list of courses and 
the list of each course taught by a particular faculty.
* Add User: Admin can add faculty or student to the database.
* View Responses : Admin can view the feedback responses of all the courses submitted by the students.
* Toggle Feedback Status: Admin can toggle the feedback status whenever required.

### Faculty :
![Screenshot from 2021-04-21 12-09-16](https://user-images.githubusercontent.com/47289942/115508041-80881f80-a29a-11eb-8278-68a36be805bf.png)
* Login : Faculty will login using the credentials given by the admin.
* View responses : Faculty can view the responses for their respective courses submitted by the students which
comprises of two parameters namely average rating and remarks.
* Create Course : Faculty needs to create the course for which he/she is willing to take feedback.
* Delete Course : Faculty can delete a course,

### Student :
![Screenshot from 2021-04-21 12-09-24](https://user-images.githubusercontent.com/47289942/115508046-81b94c80-a29a-11eb-9828-ad72a9e45f8f.png)
* Login: Student will login using the credentials given by the admin.
* Form submission: Student can visit the portal, select the course from the list of courses he/she is
enrolled in and submit the feedback. A student can submit feedback only to the courses he is
enrolled in. The student interface ensures that a student can submit feedback for a course at most
once.

### **Note : Structure for the excel files to be uploaded by the Admin is provided in the UploadFiles folder.**
### **Admin needs to strictly follow the structure provided in UploadFiles and only excel files need to be uploaded.**
