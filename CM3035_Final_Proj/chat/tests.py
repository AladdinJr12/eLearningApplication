from django.test import TestCase
from e_learning_application.models import *
from e_learning_application.factories import *
from chat.models import *
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch

# Create your tests here.
class ChatRoomTests(TestCase):
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

        #---Create a second student user and their app user instance who is not enrolled in anything--#
        self.non_enrolled_user = UserFactory(username="other_student", email="non_enrolled_user@mail.com")
        self.non_enrolled_user.set_password("Password123")
        self.non_enrolled_user.save()
        self.non_enrolled_user_app_user = AppUserFactory(user=self.non_enrolled_user, role="Student")
        self.non_enrolled_student = StudentFactory(userID=self.non_enrolled_user_app_user)

        #---Create a test course--#
        self.course = CourseFactory(teacherID=self.teacher, courseTitle="Test Course")

        #----Create an enrollment entry---#
        self.enrollment = EnrollmentsFactory(courseID=self.course, studentID= self.student)

        #----Set up chat room---#
        self.chat_room_url = reverse("chat_room", args=[self.course.pk])

    def test_teacher_can_access_chat(self):
        """Test that the teacher can access the chat room."""
        self.client.login(username="teacheruser", password="Password123")
        response = self.client.get(self.chat_room_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "chat/chat_room.html")

    @patch("chat.views.requests.post")  # Mock API call
    def test_enrolled_student_can_access_chat(self, mock_post):
        """Test that an enrolled student can access the chat room."""
        mock_post.return_value.status_code = 201  # Simulate API success
        
        self.client.login(username="studentuser", password="Password123")
        response = self.client.get(self.chat_room_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "chat/chat_room.html")

    def test_non_enrolled_student_cannot_access_chat(self):
        """Test that a non-enrolled student gets forbidden access."""
        self.client.login(username="other_student", password="Password123")
        response = self.client.get(self.chat_room_url)
        self.assertEqual(response.status_code, 403)

    @patch("chat.views.requests.post")  # Mock it in the correct module
    def test_status_update_is_sent(self, mock_post):
        """Test that a status update is sent when a student enters the chat."""
        mock_post.return_value.status_code = 201  # Simulate a successful API response

        self.client.login(username=self.student.userID.user.username, password="Password123")
        response = self.client.get(self.chat_room_url)

        # Ensure chat room loads + user is redirected to it
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "chat/chat_room.html")
        # Verify API call was made
        mock_post.assert_called_once()
