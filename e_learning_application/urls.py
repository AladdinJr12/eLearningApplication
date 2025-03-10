from django.urls import include, path
from . import views #--Importing from views.py--//
from . import api   #Importing from api.py---//
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from e_learning_application.views import api_status_update
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView



urlpatterns =[
    path ('', views.index, name='index' ),
    path ('create-new-account/', views.create, name='create'),
    path ('login/', views.user_login, name='login'),
    path ('courses/', views.courses, name='courses'),
    path ('logout/', views.user_logout, name='logout'),
    path('student_dashboard/<int:appUser_id>', views.studentHomepage, name= 'student_dashboard'),
    path('teacher_dashboard/<int:appUser_id>', views.teacherHomepage, name= 'teacher_dashboard'),

    # Dynamic route for viewing a user's homepage
    path('user/<int:appUser_id>/', views.userHomepage, name='user_homepage'),

    path('create-course/', views.create_course, name='create_course'),
    path('delete-course/<int:course_id>/', views.delete_course, name='delete_course'),
    path('add-content/', views.add_content, name='add_content'),
    path('delete-content/<int:content_id>', views.delete_content, name='delete_content'),
    path('enroll/<int:course_id>/', views.enroll_in_course, name='enroll_in_course'),
    path('unenroll/<int:course_id>/', views.unenroll_from_course, name='unenroll_from_course'),
    path('unenroll/<int:course_id>/<int:student_id>', views.removed_from_course, name='removed_from_course'),
    path('course-content/<int:course_id>/', views.course_content, name='course_content'),
    path('search-user/', views.search_user, name='search_user'),
    path('error/', views.error_page, name='error_page'),
    path('status-page/', views.status_page, name='status_page'),
    path('status-form-page/', views.status_form_page, name='status_form_page'),
    path('check-new-status-updates/', check_new_status_updates, name='check_new_status_updates'),

    #---for the chat room---#
    path('chat/', include('chat.urls')), 
    #----Api endpoints----#
    path("api/status-update/", api_status_update, name="api_status_update"),
    # Swagger documentation endpoints
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
] 


