from django.urls import re_path
from cromwellapp import consumers

websocket_urlpatterns = [
    re_path(r'ws/cromwell/app/', consumers.ChatConsumer.as_asgi()),
]