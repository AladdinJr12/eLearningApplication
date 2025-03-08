#----Serializers for creating an entry of each model:

from rest_framework import serializers

from .models import *

class AppUserSerializer(serializers.ModelSerializer):
    # You can nest the built-in User serializer if needed or expose selected fields
    class Meta:
        model = AppUser
        fields = ['id', 'user', 'role']
        # If you want to include details from the related User model, you can use nested serializers.

class TeacherSerializer(serializers.ModelSerializer):
    #----Include nested AppUser details
    user = AppUserSerializer(source='userID', read_only=True)
    
    class Meta:
        model = Teachers
        fields = ['teacherID', 'user']
        # Use source if you want to rename or nest fields

class StudentSerializer(serializers.ModelSerializer):
    user = AppUserSerializer(source='userID', read_only=True)
    
    class Meta:
        model = Students
        fields = ['studentID', 'user']

class CourseSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer(source='teacherID', read_only=True)
    
    class Meta:
        model = Course
        fields = ['courseID', 'teacher', 'courseTitle', 'courseDescription', 'courseCreatedDate']

class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(source='courseID', read_only=True)
    student = StudentSerializer(source='studentID', read_only=True)
    
    class Meta:
        model = Enrollments
        fields = ['enrollmentID', 'course', 'student', 'enrollment_date']

class FeedbackSerializer(serializers.ModelSerializer):
    course = CourseSerializer(source='courseID', read_only=True)
    student = StudentSerializer(source='studentID', read_only=True)
    
    class Meta:
        model = Feedback
        fields = ['feedbackID', 'course', 'student', 'feedbackText', 'date_of_feedback']

class StatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusUpdates
        fields = ["user_id", "status_content", "status_update_date"]









