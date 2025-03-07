from django.urls import path, re_path
from .views import chat_room
from . import consumers

urlpatterns = [
   path('room/<int:course_id>/', chat_room, name='chat_room'),
]

