from django.urls import re_path
from cromwellapp import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/roomName/', consumers.ChatConsumer.as_asgi()),
]