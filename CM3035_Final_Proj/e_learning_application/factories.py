#---Factories for unit testing purposes---------#
import factory
from django.contrib.auth.models import User
from faker import Faker
from .models import *
from chat.models import *
from django.utils import timezone

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall('set_password', 'password123')


class AppUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AppUser

    user = factory.SubFactory(UserFactory)
    role = "Student"  # or "Teacher": Note to self that this can be adjusted in tests.py


class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Students
    userID = factory.SubFactory(AppUserFactory)


class TeacherFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Teachers
    userID = factory.SubFactory(AppUserFactory)


class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Course
    courseTitle = factory.Faker("sentence", nb_words=4)
    teacherID = factory.SubFactory(TeacherFactory)

class CourseContentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CourseContent
    
    contentTitle = factory.Sequence(lambda n: f'Content {n}')
    course = factory.SubFactory(CourseFactory)
    teacher = factory.SubFactory(TeacherFactory)
    file = None  # Default to no file

class EnrollmentsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Enrollments
    studentID = factory.SubFactory(StudentFactory)
    courseID = factory.SubFactory(CourseFactory)

class FeedbackFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Feedback
    courseID = factory.SubFactory(CourseFactory)
    studentID = factory.SubFactory(StudentFactory)
    feedbackText = "This is a sample feedback."
    date_of_feedback = factory.Faker('date_object')


class StatusUpdatesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StatusUpdates
    user_id = factory.SubFactory(AppUserFactory)
    status_content = factory.Faker("sentence", nb_words=10)
    status_update_date = factory.LazyFunction(timezone.now)
    is_read = False


class ChatMessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ChatMessage

    sender = factory.SubFactory(UserFactory)
    receiver = factory.SubFactory(UserFactory)
    message = factory.Faker("sentence")
    timestamp = factory.Faker("date_time")