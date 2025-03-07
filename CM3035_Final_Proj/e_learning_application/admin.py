from django.contrib import admin

#---Register your models here so that they can be viewed via the admin page---#
from .models import *

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("courseID", "courseTitle", "teacherID", "courseCreatedDate")
    search_fields = ("courseTitle", "teacherID__name")  # Allows searching by title or teacher
    list_filter = ("courseCreatedDate",)
    ordering = ("-courseCreatedDate",)  # Show newest courses first

@admin.register(CourseContent)
class CourseContentAdmin(admin.ModelAdmin):
    list_display = ("contentID", "contentTitle" , "course", "file", "date_added", "teacher")
    search_fields = ("course", "contentTitle", "teacher")
    list_filter = ("date_added",)
    ordering= ("-date_added",)


@admin.register(Enrollments)
class EnrollmentsAdmin(admin.ModelAdmin):
    list_display = ('enrollmentID', 'courseID', 'studentID', 'enrollment_date')





# @admin.register(Lesson)
# class LessonAdmin(admin.ModelAdmin):
#     list_display = ("lessonID", "course", "added_date")
#     search_fields = ("course__courseTitle",)
#     list_filter = ("added_date",)

# @admin.register(McqQuestion)
# class McqQuestionAdmin(admin.ModelAdmin):
#     list_display = ("questionID", "lesson", "question_content")
#     search_fields = ("lesson__course__courseTitle", "question_content")
#     list_filter = ("lesson__course",)

# @admin.register(Answer)
# class AnswerAdmin(admin.ModelAdmin):
#     list_display = ("answerID", "related_question", "answer_text", "is_correct")
#     search_fields = ("related_question__question_content", "answer_text")
#     list_filter = ("is_correct",)

