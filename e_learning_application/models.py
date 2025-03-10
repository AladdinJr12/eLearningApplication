from django.db import models

# Create your models here.
#-----For setting up user accounts---#
from django.contrib.auth.models import User
#----For setting up contraints for cases where the same user cant enroll into the same course etc-----#
from django.db.models import UniqueConstraint
#----------For error handling----------#
from django.core.exceptions import ValidationError


#---For defining roles choices for my E-Learning applications---#
ROLE_CHOICES = [
    ('Teacher', 'Teacher'),
    ('Student', 'Student'),
]


#____________________________--------Models for the users------------___________________________#

class AppUser(models.Model):
    role = models.TextField(max_length=10, choices=ROLE_CHOICES)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #---The django User contains the fields username, email, password and id)--#
    #---So they can be accessed via user.username, user.email etc-----# 

    def __str__(self):
        return  f"{self.user.username} ({self.role})"


class Teachers(models.Model):
    teacherID = models.AutoField(primary_key=True)
    userID = models.ForeignKey(AppUser, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        #----Ensure the linked AppUser has the role 'teacher'-----#
        if self.userID.role != 'Teacher':
            raise ValueError("Only users with the role 'Teacher' can be added to the Teachers model.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.userID.user.username} (Teacher)"
    
class Students(models.Model):
    studentID = models.AutoField(primary_key=True)
    userID = models.ForeignKey(AppUser, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        #----Ensure the linked AppUser has the role 'teacher'-----#
        if self.userID.role != 'Student':
            raise ValueError("Only users with the role 'Student' can be added to the Students model.")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.userID.user.username} (Student)"

#________-----Models for the courses, enrolled courses + feedback for courses-----_________#
class Course(models.Model):
    courseID = models.AutoField(primary_key=True)
    teacherID = models.ForeignKey(Teachers, on_delete=models.SET_NULL, null=True)
    courseTitle = models.TextField(max_length=256, null=False)
    courseDescription = models.TextField(max_length=256, null=False)
    courseCreatedDate = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Course Title: {self.courseTitle}"


class CourseContent(models.Model):
    contentID = models.AutoField(primary_key=True)
    contentTitle = models.TextField(max_length=256, null=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="courseContent")
    file = models.FileField(upload_to='course_files/', null=True, blank=True)  #--Field for file uploads--#
    date_added = models.DateTimeField(auto_now_add=True)
    teacher = models.ForeignKey(Teachers, on_delete=models.DO_NOTHING, related_name="teacher")
    #---Note for future use: to access teacher's username = course_content.teacher.userID.user.username--#

    def __str__(self):
        return f"Content for {self.course.courseTitle}"


class Enrollments(models.Model):
    enrollmentID = models.AutoField(primary_key = True)
    courseID = models.ForeignKey(Course, on_delete=models.CASCADE)
    studentID = models.ForeignKey(Students, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)
    class Meta:
        constraints = [
            UniqueConstraint(
                #---Ensures unique combination of studentID and courseID----#
                fields=['studentID', 'courseID'],  
                #---Name of the constraint---#
                name='unique_student_course'  
            )
        ]
        
    def __str__(self):
        return f"{self.studentID.userID.user.username} enrolled in {self.courseID.courseTitle}"


class Feedback(models.Model):
    feedbackID = models.AutoField(primary_key = True)
    courseID = models.ForeignKey(Course, on_delete=models.CASCADE)
    studentID = models.ForeignKey(Students, on_delete=models.CASCADE)
    feedbackText = models.TextField(max_length=256, null=False, blank= False)
    date_of_feedback = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        #---Check if said student is enrolled in said course-------------#
        if not Enrollments.objects.filter(studentID=self.studentID, courseID=self.courseID).exists():
            raise ValidationError("Only enrolled students can submit feedback for this course.")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Feedback by {self.studentID.userID.user.username} for {self.courseID.courseTitle}"



#________----------models for the application's other functionalities----------------__________#
class StatusUpdates(models.Model):
    statusUpdatesId = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    status_content = models.TextField(max_length=256, null=False, blank=False)
    status_update_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Status update by {self.user_id.user.username} on {self.status_update_date}"



    









