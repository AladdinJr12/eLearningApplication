#---routing for the chatroom
# from django.urls import re_path
# from .consumers import ChatConsumer

# websocket_urlpatterns = [
#     re_path(r"ws/chat/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
# ]

from django.urls import re_path
from channels.routing import ProtocolTypeRouter, URLRouter
from chat.consumers import ChatConsumer  # Import your WebSocket consumer
from channels.auth import AuthMiddlewareStack

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<course_id>\w+)/$", ChatConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})



