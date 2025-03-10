from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from e_learning_application.models import *
from e_learning_application.factories import *
from e_learning_application.forms import *
from unittest.mock import patch
from rest_framework import status
# Create your tests here.

#--Just chat.views() and left for testing---#

#---Checking that the error_page() function is working---#
class ErrorPageTests(TestCase):
    def test_error_page_status_code(self):
        response = self.client.get(reverse('error_page'))
        self.assertEqual(response.status_code, 200)

    def test_error_page_template(self):
        response = self.client.get(reverse('error_page'))
        self.assertTemplateUsed(response, 'e_learning_application/errorPage.html')


class TeacherRequiredTests(TestCase):
    def setUp(self):
        # Create a student user and app_user using factories
        self.student_user = UserFactory(username='student', password='Pass123')
        self.student_app_user = AppUserFactory(user=self.student_user, role='Student')

        # Create a teacher user and app_user using factories
        self.teacher_user = UserFactory(username='teacher', password='Pass123')
        self.teacher_app_user = AppUserFactory(user=self.teacher_user, role='Teacher')

    def test_student_redirected_from_teacher_page(self):
        self.client.login(username='student', password='Pass123')
        response = self.client.get(reverse('teacher_dashboard', kwargs={'appUser_id': self.teacher_app_user.id}))
        self.assertRedirects(response, reverse('error_page'))

    #---Accessing teacher_dashboard via teacher account---#
    def test_accessing_teacher_dashboard_from_teacher_account(self):
        self.client.login(username='teacher', password='Pass123')
        response = self.client.get(reverse('teacher_dashboard', kwargs={'appUser_id': self.teacher_app_user.id}))
        #---This checks if the response is successful---#
        self.assertEqual(response.status_code, 200) 
        
#-----Does the same thing as TeacherRequiredTests but for the student_required function instead------#
class StudentRequiredTests(TestCase):
    def setUp(self):
        # Create a user and app_user and student object using factories
        self.student_user = UserFactory(username='student', password='Pass123')
        self.student_app_user = AppUserFactory(user=self.student_user, role='Student')
        self.student = StudentFactory(userID= self.student_app_user)

        # Create a teacher user and app_user using factories
        self.teacher_user = UserFactory(username='teacher', password='Pass123')
        self.teacher_app_user = AppUserFactory(user=self.teacher_user, role='Teacher')

    #---Accessing student_dashboard via teacher account: essential for when teachers want to view a specific student's homepage---#
    def test_accessing_student_dashboard_from_teacher_account(self):
        self.client.login(username='teacher', password='Pass123')
        response = self.client.get(reverse('student_dashboard', kwargs={'appUser_id': self.student_app_user.id}))
        self.assertEqual(response.status_code, 200) 


    #---Accessing student_dashboard via student account---#
    def test_accessing_student_dashboard_from_student_account(self):
        self.client.login(username='student', password='Pass123')
        response = self.client.get(reverse('student_dashboard', kwargs={'appUser_id': self.student_app_user.id}))
        #---This checks if the response is successful---#
        self.assertEqual(response.status_code, 200) 

# ---testing for the index function ---#    
class IndexTests(TestCase):
    def setUp(self):
        # Create a user and app_user and student object using factories
        self.student_user = UserFactory(username='student', password='Pass123')
        self.student_app_user = AppUserFactory(user=self.student_user, role='Student')
        self.student = StudentFactory(userID= self.student_app_user)

        # Create a teacher user and app_user using factories
        self.teacher_user = UserFactory(username='teacher', password='Pass123')
        self.teacher_app_user = AppUserFactory(user=self.teacher_user, role='Teacher')
    
    def test_accessing_index_as_student(self):
        self.client.login(username='student', password='Pass123')
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, reverse('student_dashboard', kwargs={'appUser_id': self.student_app_user.id}))
    
    def test_accessing_index_as_teacher(self):
        self.client.login(username='teacher', password='Pass123')
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, reverse('teacher_dashboard', kwargs={'appUser_id': self.teacher_app_user.id}))

    def test_accessing_index_as_unauthenticated_user(self):
        #--Ensure the user is logged out--#
        self.client.logout()

        #---Make a GET request to the index page---#
        response = self.client.get(reverse('index'))

        #---Check that the response status code is 200 (OK)---#
        self.assertEqual(response.status_code, 200)

        #---Check that the correct template is used---#
        self.assertTemplateUsed(response, 'e_learning_application/MainHomepage.html')



#----test creating a user----#
class UserRegistrationTests(TestCase):
    def test_create_user_valid(self):
        response = self.client.post(reverse('create'), {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'Password123',
            'role': 'Student'
        })
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Students.objects.count(), 1)
        self.assertRedirects(response, reverse('login'))


#---testing logging in----#
class LoginTests(TestCase):
    def setUp(self):
        self.student_user = UserFactory(username='testuser', email='testuser1@mail.com', password='Password123')
        self.student_app_user = AppUserFactory(user=self.student_user, role='Student')
        self.student = StudentFactory(userID= self.student_app_user)

    def test_valid_login(self):
        response = self.client.post(reverse('login'), {'role': 'Student', 'email': 'testuser1@mail.com', 'password': 'Password123'})
        self.assertEqual(response.status_code, 302)  # Redirect after login

    def test_invalid_login(self):
        response = self.client.post(reverse('login'), {'role': 'Student', 'email': 'testuser1@mail.com', 'password': 'wrongpassword123'})
        self.assertContains(response, "Invalid email or password.")


#---testing the courses() function which returns the general courses view page---#
class CoursesTests(TestCase):
    def test_accessing_courses_page(self):
        #---Make a GET request to the courses page---#
        response = self.client.get(reverse('courses'))

        #---Check that the response status code is 200 (OK)---#
        self.assertEqual(response.status_code, 200)

        #---Check that the correct template is used---#
        self.assertTemplateUsed(response, 'e_learning_application/courses.html')    


#---testing for the student and teacher dashboards---#
class DashboardsTests(TestCase):
    def setUp(self):
        # Create a user and app_user and student object using factories
        self.student_user = UserFactory(username='student', password='Pass123')
        self.student_app_user = AppUserFactory(user=self.student_user, role='Student')
        self.student = StudentFactory(userID= self.student_app_user)

        # Create a teacher user and app_user using factories
        self.teacher_user = UserFactory(username='teacher', password='Pass123')
        self.teacher_app_user = AppUserFactory(user=self.teacher_user, role='Teacher')
    
    def test_teacher_dashboard(self):
        self.client.login(username='teacher', password='Pass123')
        response = self.client.get(reverse('teacher_dashboard', kwargs={'appUser_id': self.teacher_app_user.id}))
        self.assertTemplateUsed(response, 'e_learning_application/TeacherHomepage.html')

    def test_student_dashboard(self):
        self.client.login(username='student', password='Pass123')
        response = self.client.get(reverse('student_dashboard', kwargs={'appUser_id': self.student_app_user.id}))
        self.assertTemplateUsed(response, 'e_learning_application/StudentHomepage.html')

class CourseManagementTests(TestCase):
    def setUp(self):
        """Set up test users and courses."""
        #---Create a teacher user and their app user instance---#
        self.teacher_user = UserFactory(username="teacheruser", email="teacher@mail.com")
        self.teacher_user.set_password("Password123")
        self.teacher_user.save()
        self.teacher_app_user = AppUserFactory(user=self.teacher_user, role="Teacher")
        self.teacher = TeacherFactory(userID=self.teacher_app_user)

        #---Creates a second teacher user and their app user instance----#
        self.teacher_user2 = UserFactory(username="teacheruser2", email="teacher2@mail.com")
        self.teacher_user2.set_password("Password123")
        self.teacher_user2.save()
        self.teacher_app_user2 = AppUserFactory(user=self.teacher_user2, role="Teacher")
        self.teacher2 = TeacherFactory(userID=self.teacher_app_user2)

        #---Create a student user and their app user instance--#
        self.student_user = UserFactory(username="studentuser", email="student@mail.com")
        self.student_user.set_password("Password123")
        self.student_user.save()
        self.student_app_user = AppUserFactory(user=self.student_user, role="Student")
        self.student = StudentFactory(userID=self.student_app_user)

        #---Create a second student user and their app user instance--#
        self.student_user2 = UserFactory(username="studentuser2", email="student@mail.com")
        self.student_user2.set_password("Password123")
        self.student_user2.save()
        self.student_app_user2 = AppUserFactory(user=self.student_user2, role="Student")
        self.student2 = StudentFactory(userID=self.student_app_user2)

        #---Create a test course--#
        self.course = CourseFactory(teacherID=self.teacher)

        #--Create a test course content--#
        self.content = CourseContentFactory(course=self.course, teacher=self.teacher)

        #----Create an enrollment entry---#
        self.enrollment = EnrollmentsFactory(courseID=self.course, studentID= self.student2)

    #---test that only teachers can create courses---#
    def test_teacher_can_create_course(self):
        """Verify that a teacher can successfully create a course."""
        self.client.login(username="teacheruser", password="Password123")
        response = self.client.post(reverse("create_course"), {
            "courseTitle": "New Course",
            "courseDescription": "This is a test course",
        })
        self.assertEqual(Course.objects.count(), 2)  #---2 here as 1 was created in setUp---#
        self.assertRedirects(response, reverse("add_content"))

    def test_student_cannot_create_course(self):
        """Verify that a student cannot create a course."""
        self.client.login(username="studentuser", password="Password123")
        response = self.client.post(reverse("create_course"), {
            "courseTitle": "Unauthorized Course",
            "courseDescription": "Should not be created",
        })
        self.assertEqual(Course.objects.count(), 1)  #---No new course should be created--#
        self.assertEqual(response.status_code, 302)  #--PermissionDenied and redirected to error page--#
        self.assertRedirects(response, reverse('error_page'))

    #---test that only teachers can create/add course content---#
    @patch("requests.post")  # Mock the API request
    def test_teacher_can_add_content(self, mock_post):
        """Verify that a teacher can add content to their course."""
        self.client.login(username="teacheruser", password="Password123")
        file_mock = SimpleUploadedFile("test.pdf", b"Test content", content_type="application/pdf")

        #---Simulate a successful API response---#
        mock_post.return_value.status_code = 200

        response = self.client.post(reverse("add_content"), {
            "contentTitle": "Test Content",
            "course": self.course.courseID,
            "file": file_mock,
        })

        self.assertEqual(CourseContent.objects.count(), 2)   #---2 here as 1 was created in setUp---#
        self.assertRedirects(response, reverse("teacher_dashboard", kwargs={'appUser_id': self.teacher_app_user.id}))

        #---Ensures that the API request was called---#
        self.assertTrue(mock_post.called)

    def test_student_cannot_add_content(self):
        """Ensure that a student cannot add content to a course."""
        self.client.login(username="studentuser", password="Password123")
        file_mock = SimpleUploadedFile("test.pdf", b"Test content", content_type="application/pdf")

        response = self.client.post(reverse("add_content"), {
            "contentTitle": "Unauthorized Content",
            "course": self.course.courseID,
            "file": file_mock,
        })

        self.assertEqual(CourseContent.objects.count(), 1)  # No new content should be created
        self.assertEqual(response.status_code, 302)  #--PermissionDenied and redirected to error page--#
        self.assertRedirects(response, reverse('error_page'))
    
    #----Tests for the delete_content () function---#
    def test_teacher_can_delete_content(self):
        """Ensure that a teacher can delete their own content."""
        self.client.login(username="teacheruser", password="Password123")
        response = self.client.post(reverse("delete_content", args=[self.content.contentID]))
        
        self.assertEqual(CourseContent.objects.count(), 0)  #--Content should be deleted--#
        self.assertRedirects(response, reverse("course_content", args=[self.course.courseID]))

    def test_student_cannot_delete_content(self):
        """Ensure that a student cannot delete content."""
        self.client.login(username="studentuser", password="Password123")
        response = self.client.post(reverse("delete_content", args=[self.content.contentID]))

        self.assertEqual(CourseContent.objects.count(), 1)  # Content should NOT be deleted
        self.assertEqual(response.status_code, 302)  #--PermissionDenied and redirected to error page--#
        self.assertRedirects(response, reverse('error_page'))

    #---testing for the delete course function----#
    def test_teacher_can_delete_course_created_by_themselves(self):
        """Ensure a teacher can delete a course they created."""
        self.client.login(username="teacheruser", password="Password123")

        response = self.client.post(reverse("delete_course", args=[self.course.pk]))

        self.assertEqual(Course.objects.count(), 0)  # Course should be deleted
        self.assertRedirects(response, reverse("teacher_dashboard", kwargs={'appUser_id': self.teacher_app_user.id}))
    
    def test_student_cannot_delete_course(self):
        """Ensure a student cannot delete a course."""
        self.client.login(username="studentuser", password="Password123")

        response = self.client.post(reverse("delete_course", args=[self.course.pk]))
        
        self.assertEqual(Course.objects.count(), 1)  # Course should still exist
        self.assertEqual(response.status_code, 302)  #--PermissionDenied and redirected to error page--#
        self.assertRedirects(response, reverse('error_page'))

    def test_teacher_cannot_delete_course_created_by_others(self):
        """Ensure a teacher can delete a course they did not create."""
        self.client.login(username="teacheruser2", password="Password123")

        response = self.client.post(reverse("delete_course", args=[self.course.pk]))

        self.assertEqual(Course.objects.count(), 1)  # Course should be deleted
         #--PermissionDenied: Note that there is no redirect since logged in user is a teacher---#
        self.assertEqual(response.status_code, 403) 
    
    #--Testing the remove student from course functionality---#
    def test_teacher_can_remove_student_from_course(self):
        """Ensure a teacher can remove a student from their course."""
        self.client.login(username="teacheruser", password="Password123")

        # Enroll 1 student first: So the course will now have 2 enrolled students (One from setup)
        enrollment = Enrollments.objects.create(studentID=self.student, courseID=self.course)

        response = self.client.post(reverse("removed_from_course", args=[self.course.pk, self.student.pk]))
        
        #--1 student should be removed:so back to just 1 student left in course --#
        self.assertEqual(Enrollments.objects.count(), 1) 
        self.assertRedirects(response, reverse("course_content", args=[self.course.pk]))


    #---_____________Testing for enrollments________---#
    @patch("requests.post")  # Mock the API request
    def test_student_can_enroll_in_course(self, mock_post):
        """Ensure a student can enroll in a course."""
        self.client.login(username="studentuser", password="Password123")

        # Mock successful API response
        mock_post.return_value.status_code = 200

        response = self.client.post(reverse("enroll_in_course", args=[self.course.pk]))

        self.assertEqual(Enrollments.objects.count(), 2)  #--Student should be enrolled: 2 here since 1 enrollment was created earlier--#
        self.assertRedirects(response, reverse("course_content", args=[self.course.pk]))
        self.assertTrue(mock_post.called)


    def test_student_can_unenroll_from_course(self):
        """Ensure a student can unenroll from a course."""
        self.client.login(username="studentuser2", password="Password123")

        #---Removing the enrollment entry created at setup--#
        response = self.client.post(reverse("unenroll_from_course", args=[self.course.pk]))
        
        #--1 student should be removed:so back to just 0 student left in course --#
        self.assertEqual(Enrollments.objects.count(), 0)  
        self.assertRedirects(response, reverse("student_dashboard", kwargs={'appUser_id': self.student_app_user2.id}))

    #---testing the search functionality---#
    def test_search_user(self):
        response = self.client.get(reverse('search_user') + '?searched_user=studentuser2')
        self.assertEqual(response.status_code, 200) #--These two lines ensures that it is working--#
        self.assertIn('searched_users', response.context) 
        self.assertEqual(len(response.context['searched_users']), 1) #--This means that we found 1 user which is true--#

#---Testing course content---#
class CourseContentTests(TestCase):
    def setUp(self):
        """Set up test users and courses."""
        #---Create a teacher user and their app user instance---#
        self.teacher_user = UserFactory(username="teacheruser", email="teacher@mail.com")
        self.teacher_user.set_password("Password123")
        self.teacher_user.save()
        self.teacher_app_user = AppUserFactory(user=self.teacher_user, role="Teacher")
        self.teacher = TeacherFactory(userID=self.teacher_app_user)

        #---Create a student user and their app user instance--#
        self.student_user = UserFactory(username="studentuser", email="student@mail.com")
        self.student_user.set_password("Password123")
        self.student_user.save()
        self.student_app_user = AppUserFactory(user=self.student_user, role="Student")
        self.student = StudentFactory(userID=self.student_app_user)

        #---Create a test course--#
        self.course = CourseFactory(teacherID=self.teacher, courseTitle="Test Course")

        #--Create a test course content--#
        self.content = CourseContentFactory(course=self.course, teacher=self.teacher, contentTitle="Lesson 1")

        #----Create an enrollment entry---#
        self.enrollment = EnrollmentsFactory(courseID=self.course, studentID= self.student)

    def test_teacher_can_view_course_content(self):
        """Ensure a teacher can access course content."""
        self.client.login(username="teacheruser", password="Password123")
        response = self.client.get(reverse("course_content", args=[self.course.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "e_learning_application/courseContent.html")
        self.assertContains(response, "Lesson 1")  # Ensure content is displayed

    def test_student_can_view_course_content(self):
        """Ensure a student can access course content."""
        self.client.login(username="studentuser", password="Password123")
        response = self.client.get(reverse("course_content", args=[self.course.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Lesson 1")  # Student should see course content

    def test_student_can_submit_feedback(self):
        """Ensure a student can submit feedback."""
        self.client.login(username="studentuser", password="Password123")
        
        feedback_data = {"feedbackText": "Great course!"}
        response = self.client.post(reverse("course_content", args=[self.course.pk]), feedback_data)

        self.assertEqual(Feedback.objects.count(), 1)  # Feedback should be saved
        self.assertRedirects(response, reverse("course_content", args=[self.course.pk]))


#-----testing the status------#
class StatusTests(TestCase):
    def setUp(self):
        """Set up test users and courses."""
        #---Create a teacher user and their app user instance---#
        self.teacher_user = UserFactory(username="teacheruser", email="teacher@mail.com")
        self.teacher_user.set_password("Password123")
        self.teacher_user.save()
        self.teacher_app_user = AppUserFactory(user=self.teacher_user, role="Teacher")
        self.teacher = TeacherFactory(userID=self.teacher_app_user)

        #---Create a student user and their app user instance--#
        self.student_user = UserFactory(username="studentuser", email="student@mail.com")
        self.student_user.set_password("Password123")
        self.student_user.save()
        self.student_app_user = AppUserFactory(user=self.student_user, role="Student")
        self.student = StudentFactory(userID=self.student_app_user)

        #---Create a test course--#
        self.course = CourseFactory(teacherID=self.teacher)

        #---create a status update---#
        self.status_update = StatusUpdatesFactory(user_id= self.teacher_app_user)

    def test_status_page(self):
        """Ensure a user can enter the status page"""
        self.client.login(username="teacheruser", password="Password123")
        response = self.client.get(reverse('status_page'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('status_list', response.context)
        self.status_update.refresh_from_db()
        self.assertTrue(self.status_update.is_read)

    
    def test_check_new_status_updates(self):
        """Checks that the notification button is working"""
        self.client.login(username='teacheruser', password='Password123')
        response = self.client.get(reverse('check_new_status_updates'))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'has_new_updates': True})

        self.status_update.is_read = True
        self.status_update.save()
        response = self.client.get(reverse('check_new_status_updates'))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'has_new_updates': False})


    def test_create_status_update(self):
        """Checks that the Api status update is working"""
        self.client.login(username='studentuser', password='Password123')
        data = {
            'user_id': self.student_user.id,
            'receiver_id': self.student_user.id,
            'course_id': self.course.courseID,
            'message': 'New Status'
        }

        response = self.client.post(reverse('api_status_update'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) #-- This means that server has successfully creatdd new resource--#
        self.assertEqual(response.data['status_content'], 'New Status')
        self.assertEqual(StatusUpdates.objects.count(), 2)  #---2 because 1 created here and 1 from setup---#

    def test_create_status_update_missing_fields(self):
        """Checks that the Api status update will not go through if there are missing fields"""
        data = {
            'user_id': self.student_user.id,
            'course_id': self.course.courseID
        }
        self.client.login(username='studentuser', password='Password123')
        response = self.client.post(reverse('api_status_update'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    

    def test_status_form_submission(self):
        """Checks that status form is accessible and works"""
        # Log in as the student user
        self.client.login(username='studentuser', password='Password123')

        # Get the form page to retrieve the CSRF token
        response = self.client.get(reverse('status_form_page'))
        csrf_token = response.context['csrf_token']

        # Prepare form data with CSRF token
        form_data = {
            'csrfmiddlewaretoken': csrf_token,
            'status_content': 'Test status',  # Ensure this matches the form field name
        }

        # Submit the form data
        response = self.client.post(reverse('status_form_page'), data=form_data)

        # Check if the status update was saved in the database
        self.assertTrue(StatusUpdates.objects.filter(status_content='Test status').exists())

    def test_invalid_status_form(self):
        response = self.client.post(reverse('status_form_page'), {'status_content': ''})
        self.assertFormError(response, 'status_form', 'status_content', 'This field is required.')



    


    

    

