from django.urls import path
from .views import *

urlpatterns = [

    path("api/tasks/",TaskListCreateAPIView.as_view()),

    path("api/tasks/<int:pk>/",TaskDetailAPIView.as_view()),

    path("tasks/create/", create_task_page, name="create-task-page"),

    path("task-detail/", task_detail_page, name="task-detail"),

    path("task-edit/", task_edit_page, name="task-edit"),

    path("notifications/", NotificationListAPIView.as_view()),

    path("notifications/count/", NotificationCountAPIView.as_view()),

    path("notifications/<int:pk>/read/", MarkNotificationReadAPIView.as_view()),

    path("api/chat/messages/", ChatMessageListAPIView.as_view()),
]



