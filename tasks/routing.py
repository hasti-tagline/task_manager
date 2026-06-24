from django.urls import path, re_path
from .consumers import TaskConsumer, ChatConsumer

websocket_urlpatterns = [
    # Task updates (based on task_id)
   path("ws/tasks/<int:user_id>/", TaskConsumer.as_asgi()),

    # Chat for a task
    path("ws/chat/<int:task_id>/", ChatConsumer.as_asgi()),
]