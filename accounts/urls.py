from django.urls import path
from .views import *

urlpatterns = [

    path("api/register/",RegisterAPIView.as_view()),

    path("api/users/",UserListAPIView.as_view(),name="users"),

    path("api/users/<int:pk>/user/",UserDetailAPIView.as_view(),name="user-detail"),
    path("api/users/<int:user_id>/tasks/",UserTaskListAPIView.as_view(),name="user-tasks"),
    
    path("user-detail/", user_detail_page, name="user-detail-page"),
    

    path("chat/",chat_page,name="chat-page"),

]

