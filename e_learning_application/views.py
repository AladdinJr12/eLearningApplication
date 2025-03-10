
from django.shortcuts import render, redirect, get_object_or_404

#---imports for creating users + login functionalitu---#
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

#---for retricting certain pages to just logged in students/teachers---#
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

#---for passsing in messages such as "successful account creation"----#
from django.contrib import messages

#-----importing the database tables/models---#
from .models import *

#--Importing the serializers---#
from .serializers import * 

#---Importing the forms---#
from .forms import *

#----To handle the prg problem for the feedback submission---#
from django.http import HttpResponseRedirect
from django.urls import reverse
import requests

#---for status updates----#
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from django.http import JsonResponse

#---for the search function to gather related models---#
from django.db.models import Prefetch



#---The error page for when user attempts to access pages while not logged in / logged in as the wrong user----#
def error_page(request):
    return render(request, 'e_learning_application/errorPage.html')

#------applying retrictions for pages that can only be logged in as a teacher----#
def teacher_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not hasattr(request.user, 'appuser') or request.user.appuser.role != 'Teacher':
            messages.error(request, "You do not have permission to access this page.")
            return redirect('error_page')  #----Redirect to the error page---#
        return view_func(request, *args, **kwargs)
    return _wrapped_view


#------applying retrictions for pages that can only be logged in as a student----#
def student_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not hasattr(request.user, 'appuser') or request.user.appuser.role != 'Student':
            messages.error(request, "You do not have permission to access this page.")
            return redirect('error_page')  #----Redirect to the error page---#
        return view_func(request, *args, **kwargs)
    return _wrapped_view

#---This is just for the enrollment functionality: Ensures that it only works with logged in students--#
def student_enrollment_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not hasattr(request.user, 'appuser') or request.user.appuser.role != 'Student':
            messages.error(request, "A registered student account is required to view this course ")
            return redirect('login')  #----Redirect to the login page---#
        return view_func(request, *args, **kwargs)
    return _wrapped_view


#_________-----------functions for the main pages--------------------___________#
def index(request, date_range=None):
    #---for if the user tries to access the homepage while logged in

    if request.user.is_authenticated:
        app_user = AppUser()
        try:
            app_user = AppUser.objects.get(user=request.user)
            if app_user.role == "Student":
                return redirect('student_dashboard', appUser_id=app_user.id)
            
            elif app_user.role == "Teacher":
                return redirect('teacher_dashboard', appUser_id=app_user.id)

        except AppUser.DoesNotExist:
            pass

    return render(request, 'e_learning_application/MainHomepage.html')


#-----------function for creating new account-----------------#
def create(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Create the user
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()

            # Create AppUser entry
            role = form.cleaned_data['role']
            app_user = AppUser.objects.create(user=user, role=role)

            # Create either a Student or Teacher entry
            if role == "Student":
                Students.objects.create(userID=app_user)
            elif role == "Teacher":
                Teachers.objects.create(userID=app_user)

            #---Add success message---#
            messages.success(request, "Account successfully created!")
            #---Redirects the user to the login page upon successful creation----#
            return redirect('login')  
        else:
            print(form.errors) #--For debugging purposes--#
    else:
        form = UserRegistrationForm()

    return render(request, "e_learning_application/create.html", {"form": form})


#-----------function for logging in-----------------#
def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            selected_role = form.cleaned_data['role']

            #---Retrieve the user by email-----------#
            try:
                user = User.objects.get(email=email)
                authenticated_user = authenticate(request, username=user.username, password=password)

                if authenticated_user:
                    app_user = AppUser.objects.get(user=user)

                    # Ensure the selected role matches the user's actual role
                    if selected_role == "Student" and Students.objects.filter(userID=app_user).exists():
                        login(request, authenticated_user)
                        return redirect('student_dashboard', appUser_id=app_user.id)  #-----Redirect to Student dashboard----#

                    elif selected_role == "Teacher" and Teachers.objects.filter(userID=app_user).exists():
                        login(request, authenticated_user)
                        print(f"My app_user is: {app_user.id}")
                        return redirect('teacher_dashboard', appUser_id=app_user.id)  #---Redirect to Teacher dashboard--#

                    else:
                        form.add_error(None, "You do not have access as a " + selected_role)
                else:
                    form.add_error(None, "Invalid email or password.")

            except User.DoesNotExist:
                form.add_error(None, "User does not exist.")
        else:
            print(form.errors) #--For debugging purposes--#

    else:
        form = UserLoginForm()

    return render(request, "e_learning_application/login.html", {"form": form})


#---function for logging out----#
def user_logout(request):
    logout(request)
    print("logging out now")
    #---redirect back to homepage-----#
    return redirect('index')


#---This is just the general courses view page----#
def courses(request):
    available_courses = Course.objects.all()
    # Default to general courses page if user is not a student or not logged in
    return render(request, "e_learning_application/courses.html", {'available_courses': available_courses})


#---link for the teacher's homepage----------#
@login_required (login_url='login') # Ensure user is logged in as a teacher
@teacher_required
def teacherHomepage(request, appUser_id):
    status_list = []  # --Initialize status_list to avoid UnboundLocalError--#
    try:
        # getting the logged in/searched teacher entry
        appUser = get_object_or_404(AppUser, id=appUser_id)
        #---Getting the logged in teacher entry----#
        teacher = Teachers.objects.get(userID= appUser)

        #---Getting all of the courses made by logged in teacher---#
        teacher_courses = Course.objects.filter(teacherID= teacher)

        #---Fetch the latest 3 read status updates + ensure they are arrange from newest first---#
        status_list = StatusUpdates.objects.filter(user_id=appUser, is_read=True).order_by('-status_update_date')[:3]
        print(f" our app user is {appUser}")

    except Teachers.DoesNotExist:
        teacher_courses = None

    return render(request, "e_learning_application/TeacherHomepage.html",
                   {'teacher_courses': teacher_courses,
                    'status_list': status_list,
                    'appUser': appUser
                    })


#------link for the student's homepage----------#
@login_required (login_url='login') # Ensure user is logged in as a student
def studentHomepage(request, appUser_id):
    # getting the logged in/searched teacher entry
    appUser = get_object_or_404(AppUser, id=appUser_id)
    #----Get the logged-in user’s Students object---#
    student = get_object_or_404(Students, userID= appUser)

    enrolled_courses = Course.objects.filter(enrollments__studentID=student)

    #---Fetch the latest 3 read status updates + ensure they are arrange from newest first---#
    status_list = StatusUpdates.objects.filter(user_id=appUser, is_read=True).order_by('-status_update_date')[:3]
    
    return render(request, "e_learning_application/StudentHomepage.html", 
                  {'enrolled_courses': enrolled_courses,
                    'status_list': status_list,
                    'appUser': appUser
                   })


#---so that the homepages are visible by other users---#
def userHomepage(request, appUser_id):
    search_appUser = get_object_or_404(AppUser, id=appUser_id)
    print(f"we are passing in {search_appUser}")

    if search_appUser.role == "Student":
        return redirect('student_dashboard', appUser_id=search_appUser.id)
    elif search_appUser.role == "Teacher":
        return redirect('teacher_dashboard', appUser_id=search_appUser.id)
    else:
        return render(request, 'errorPage.html')  # Handle unexpected roles



#----_______Page for creating courses and content for the courses______----------#
@login_required (login_url='login') # Ensure user is logged in
@teacher_required
def create_course(request):
    #----Get the logged-in teacher instance---#
    try: 
        teacher = Teachers.objects.get(userID = request.user.appuser)

    except Teachers.DoesNotExist:
        raise PermissionDenied("You are not logged in as a teacher")

    if request.method == "POST":
        course_form = CourseForm(request.POST)
        if course_form.is_valid():
            course = course_form.save()
            course.teacherID = teacher
            course.save()
            return redirect('add_content')  # Redirect to the lesson creation page
        else:
            print(course_form.errors) #--For debugging purposes--#

    else:
        course_form = CourseForm()

    return render(request, 'e_learning_application/createCourses.html', {'course_form': course_form})


@login_required (login_url='login') # Ensure user is logged in
@teacher_required
def add_content(request):
    app_user = AppUser.objects.get(user=request.user)
    try: 
        teacher = Teachers.objects.get(userID = request.user.appuser)

    except Teachers.DoesNotExist:
        raise PermissionDenied("You are not logged in as a teacher")

    if request.method == "POST":
        #---Note: including request.FILES for file uploads---#
        content_form = CourseContentForm(request.POST, request.FILES)  
        if content_form.is_valid():
            contentForm = content_form.save(commit=False)
            contentForm.teacher = teacher
            contentForm.save()
            enrollment_entries = Enrollments.objects.filter(courseID= contentForm.course)

            print(enrollment_entries)
            #---making status updates----#
            #----✅ Send a POST request to the API for status_update---#
            api_url = request.build_absolute_uri(reverse('api_status_update'))
            
            status_message = f"You have just added new learning material to {contentForm.course.courseTitle}!"
            # #---the first one goes to the course's teacher's account---#
            teacher_payload = {
                "user_id": request.user.appuser.id,
                "receiver_id": teacher.userID.id,
                "course_id": contentForm.course.courseID,
                "message": status_message
            }
            response = requests.post(api_url, json=teacher_payload)

            #----This goes to the student users enrolled into the course this content is added into---#
            status_message = f"New learning material has just been added to {contentForm.course.courseTitle}!"
            for entry in enrollment_entries:   
                print(entry.studentID.userID.id)
                student_payload = {
                    "user_id": request.user.appuser.id,
                    "receiver_id": entry.studentID.userID.id,
                    "course_id": contentForm.course.courseID,
                    "message": status_message
                }
                response = requests.post(api_url, json=student_payload)

            
            return redirect('teacher_dashboard', appUser_id=app_user.id)
    else:
        content_form = CourseContentForm()
    
    return render(request, 'e_learning_application/addContent.html', {'content_form': content_form})



@login_required (login_url='login') # Ensure user is logged in
@teacher_required
def delete_content(request,content_id):
    #---get the selected content---#
    content = get_object_or_404(CourseContent, contentID= content_id)
    
    #---Ensure that only the teacher who created the course can delete content---#
    if content.course.teacherID.userID != request.user.appuser:
        raise PermissionDenied("You are not allowed to delete this content.")
    
    content.delete()
    messages.success(request, "Learning material was successfully deleted!")
    return redirect('course_content', content.course.courseID)  #---Redirect to course's content page after deletion---#




#-----__________for when the user presses the enroll button____________----------#
@student_enrollment_required
def enroll_in_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    # Get the logged-in user’s Students object
    student = get_object_or_404(Students, userID= request.user.appuser.id)
    
    print("Testing for getting the course's creator")
    print(course.teacherID.userID.id)

    #---Checks whether the student is already enrolled in this course/ 
    # else it will create an  Enrollment entry---#
    enrollment, created = Enrollments.objects.get_or_create(studentID=student, courseID=course)

    if created:
        messages.success(request, "Successfully enrolled in new course!")
        print("New enrollment created!")  # Debugging message

        #----✅ Send a POST request to the API for status_update---#
        api_url = request.build_absolute_uri(reverse('api_status_update'))
        #---the first one goes to the course's teacher's account---#
        status_message = f"{request.user.username} has just enrolled into the course: {course.courseTitle}!"
        teacher_payload = {
            "user_id": request.user.appuser.id,
            "receiver_id": course.teacherID.userID.id,
            "course_id": course.courseID,
            "message": status_message
        }
        #----This goes to the student user who just enrolled---#
        status_message = f"You have just enrolled into the course: {course.courseTitle}!"
        student_payload = {
            "user_id": request.user.appuser.id,
            "receiver_id": request.user.appuser.id,
            "course_id": course.courseID,
            "message": status_message
        }

        response = requests.post(api_url, json=teacher_payload)
        response = requests.post(api_url, json=student_payload)



    #----Redirect to course content page----#
    return redirect('course_content', course_id=course.courseID)


@login_required (login_url='login') # Ensure user is logged in
def course_content(request, course_id):
    course = get_object_or_404(Course, pk= course_id)

    #---fetch the content of the course selected by the teacher--#
    content_list = CourseContent.objects.filter(course=course.courseID)

    #---fetch the enrollments matching the selected course---#
    enrollments_list = Enrollments.objects.filter(courseID= course.courseID)

    #----gather all feedbacks given for this course----#
    feedback_list = Feedback.objects.filter(courseID = course.courseID)

    #----feedback functionality (Only for students)------#
    feedback_form = None  # Default to None

    if request.user.appuser.role == "Student":  # ✅ Only allow students
        if request.method == "POST":
            feedback_form = FeedbackForm(request.POST)
            # Get the logged-in user’s Students object
            student = get_object_or_404(Students, userID= request.user.appuser.id)

            if feedback_form.is_valid():
                feedbackEntry = feedback_form.save(commit=False)
                feedbackEntry.courseID = course
                feedbackEntry.studentID = student
                feedbackEntry.save()
                # ----Redirect to prevent duplicate form submission---#
                return HttpResponseRedirect(reverse('course_content', args=[course_id]))
        else:
            feedback_form = FeedbackForm()


    return render(request, 
                  'e_learning_application/courseContent.html', 
                  {'course': course, 
                   'content_list': content_list, 
                   'enrollments_list': enrollments_list,
                   'feedback_form': feedback_form,
                   'feedback_list': feedback_list
                   })


#______--------unenroll functionality------------------___________#
@login_required (login_url='login')
@student_required
def unenroll_from_course(request, course_id):
    #---get the logged in user---#
    app_user = AppUser.objects.get(user=request.user)
    #---get the enrolled_course---#
    course = get_object_or_404(Course, pk = course_id)
    
    #---get the logged in student user ---#
    student = get_object_or_404(Students, userID= request.user.appuser.id)

    #---get the matching enrollment entry---#
    enrollment_entry = get_object_or_404(Enrollments, courseID = course, studentID= student)

    #---delete the enrollment entry----#
    enrollment_entry.delete()
    return redirect('student_dashboard', appUser_id=app_user.id) #--return to student homepage---#
  


#____-------where the teacher manually remove a student-----------_____#
@login_required (login_url='login')
@teacher_required
def removed_from_course(request, course_id, student_id):
    #--get the selected student---#
    student = get_object_or_404(Students, pk= student_id)
    print(student)

    #---get the selected course----#
    course = get_object_or_404(Course, pk=course_id)
    print(course)

    #---get the matching enrollment entry---#s
    enrollment_entry = get_object_or_404(Enrollments, courseID = course, studentID= student)

    print(enrollment_entry)

    #---ensuring that only the teacher who created the course can kick a student out of it---#
    if course.teacherID.userID != request.user.appuser:
        raise PermissionDenied("You are not allowed to delete this course")

    #----remove it----#
    enrollment_entry.delete()

    return redirect('course_content', course_id) #--return to the course content page---#


#_________--------Ability to delete course------___________#
@login_required (login_url='login')
@teacher_required
def delete_course(request, course_id):
    app_user = AppUser.objects.get(user=request.user)
    #----Get the selected course---------#
    course = get_object_or_404(Course, pk= course_id)
    
    #----Ensures that only the teacher who created the course can delete it---#
    if course.teacherID.userID != request.user.appuser:
        raise PermissionDenied("You are not allowed to delete this course")

    course.delete()

    return redirect('teacher_dashboard', appUser_id=app_user.id)


#----_________Functionality for the search button________---#
def search_user(request):
    #----Get the inputted search query---#
    query = request.GET.get('searched_user', '')

    #---get all the users---#
    users = AppUser.objects.all()

    #---find the matching appuser---#
    if query:
        users= users.filter(user__username__icontains=query)

    # Prefetch enrollments for students and their related courses
    users = users.prefetch_related(
        Prefetch(
            'students_set__enrollments_set',
            queryset=Enrollments.objects.select_related('courseID'),
            to_attr='enrollment_list'  # Custom attribute for enrollments
        ),
        Prefetch(
            'teachers_set__course_set',
            queryset=Course.objects.select_related('teacherID'),
            to_attr='created_courses_list'  # Custom attribute for enrollments
        )
    )

    return render(request, 
                  'e_learning_application/searched_results.html', 
                  {'query': query, 'searched_users':users}
                  )

    
#-------The status update page-------#
@login_required
def status_page(request):
    appUser = get_object_or_404(AppUser, user=request.user)

    #---Fetch status updates + ensure they are arrange from newest first---#
    status_list = StatusUpdates.objects.filter(user_id=appUser).order_by('-status_update_date')

    #---Mark updates as read---#
    status_list.update(is_read=True)

    return render(request, 'e_learning_application/statusPage.html', {
        'status_list': status_list
    })


#---This is the notification functrion--------------#
@login_required
def check_new_status_updates(request):
    """Check if the logged-in teacher has new status updates."""
    teacher = request.user.appuser  # Get logged-in teacher

    # Check if there are new status updates for this teacher
    new_updates = StatusUpdates.objects.filter(user_id=teacher, is_read=False).exists()

    return JsonResponse({"has_new_updates": new_updates})


#------api view + creates new status entries-----#
@api_view(["POST"])
@extend_schema(
    summary="Create a status update",
    description="Creates a new status update when a user enrolls or adds a new learning material.",
    request=StatusUpdateSerializer,
    responses={201: StatusUpdateSerializer}
)
def api_status_update(request):
    """
    API for creating a status update.
    """
    user_id = request.data.get("user_id")
    receiver_id = request.data.get("receiver_id")
    course_id = request.data.get("course_id")
    message = request.data.get("message")

    # Validate required fields
    if not all([user_id, receiver_id, course_id, message]):
        return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

    # Get necessary objects
    appUser = get_object_or_404(AppUser, pk=user_id)
    receiver = get_object_or_404(AppUser, pk=receiver_id)
    course = get_object_or_404(Course, pk=course_id)


    # Save the status update
    status_entry = StatusUpdates.objects.create(
        user_id=receiver,
        status_content=message
    )
    print(f"the receiver is: {receiver}")
    print(f"Received student status update: {message}")

    # Return the response
    serializer = StatusUpdateSerializer(status_entry)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


#----This is basically the page where user can create and post their own status updates----#
def status_form_page(request):
    if request.method =="POST":
        status_form = StatusUpdateForm(request.POST)
        if status_form.is_valid():
            statusUpdate = status_form.save(commit=False)
            statusUpdate.user_id = request.user.appuser
            statusUpdate.is_read = True
            statusUpdate.save()
            print("--we are going index after status form--")
            return redirect('index') #---returns to either teacher or student dashboard--#
        else:
            #--For debugging purposes--#
            print(request.POST)
            print("Form errors:", status_form.errors) 
    else:
        status_form = StatusUpdateForm()

    return render(request, 'e_learning_application/statusForm.html', {
        'status_form': status_form
    })





