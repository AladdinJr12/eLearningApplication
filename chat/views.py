from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ChatMessage
from e_learning_application.models import *  # Assuming courses are in this app
import requests
from django.conf import settings
from django.urls import reverse

@login_required
def chat_room(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollments_list = Enrollments.objects.filter(courseID= course.courseID)
    print(f"We are here at: {enrollments_list}")
    print(enrollments_list)
    # Ensure only enrolled students and the teacher can access
    if request.user.appuser.role == "Student":

        if not enrollments_list.filter(studentID__userID=request.user.appuser).exists():
            return HttpResponseForbidden("You are not enrolled in this course.")
        
        #--Notify the course's teacher account that someone is communicating with them---#
        course_teacher_id = course.teacherID.userID.id
        status_message = f"{request.user.username} from {course.courseTitle} has started a conversation with you!"
        api_url = request.build_absolute_uri(reverse('api_status_update'))
        print(request.user.username)
        print(status_message)
        payload = {
            "user_id": request.user.appuser.id,
            "receiver_id": course_teacher_id,
            "course_id": course.courseID,
            "message": status_message
        }

        response = requests.post(api_url, json=payload)
        
        if response.status_code == 201:
            print("✅ Status update sent successfully")
        else:
            print(f"❌ Failed to send status update: {response.text}")

    return render(request, "chat/chat_room.html", {"course": course})
