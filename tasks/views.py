from rest_framework.generics import (ListCreateAPIView,RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.shortcuts import render
from rest_framework.exceptions import ValidationError

from .models import Task,Message
from .serializers import TaskSerializer
from .tasks import send_task_email
from accounts.pagination import CustomPagination

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import get_object_or_404


from rest_framework.generics import ListAPIView,UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Notification
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from accounts.models import User




# Show all tasks and create task
class TaskListCreateAPIView(ListCreateAPIView):

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        # raise Exception("invalid data")

        user = self.request.user
        # Admin sees all tasks
        if user.role == "admin":
            queryset = Task.objects.all()

        # Manager sees tasks created by self and tasks assigned by admin
        elif user.role == "manager":
            queryset = Task.objects.filter(
                Q(created_by=user) |
                Q(assigned_to=user)
            ).distinct()

        # Employee sees assigned tasks only
        elif user.role == "employee":
            queryset = Task.objects.filter(assigned_to=user)

        else:
            queryset = Task.objects.none()

        search = self.request.GET.get("search", "")

        if search:
            queryset = queryset.filter(title__icontains=search)
        valid_statuses = [
                "pending",
                "in_progress",
                "completed",
                "review",
                "overdue",
                "rejected",
                "cancelled"
            ]

        status = self.request.GET.get("status", "")

        if status and status not in valid_statuses:
            raise ValidationError({
                "detail": ["Invalid status value"]
            })
                    
        if status:
            queryset = queryset.filter(status=status)

        return queryset.order_by("-created_at")

    def perform_create(self, serializer):
        user = self.request.user

        if user.role not in ["admin", "manager"]:
            raise PermissionError("Only Admin or Manager can create tasks")

        task = serializer.save(created_by=user)
        
        send_task_email.delay(task.id)

        channel_layer = get_channel_layer()

        for employee in task.assigned_to.all():

            Notification.objects.create(
                user=employee,
                title=f"New Task: {task.title}",
                message="You have been assigned a new task"
            )

            async_to_sync(channel_layer.group_send)(
                f"user_{employee.id}",
                {
                    "type": "task_assigned",
                    "data": {
                        "id": task.id,
                        "title": task.title,
                        "status": task.status,
                        "message": "New Task Assigned"
                    }
                }
            )


# Show, Update, Delete task
class TaskDetailAPIView(RetrieveUpdateDestroyAPIView):
   
    queryset = Task.objects.all() 
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]



    def perform_update(self, serializer):

        submission_file = self.request.FILES.get("submission")

        task = serializer.save()

        channel_layer = get_channel_layer() 

        # Existing status update notification
        for employee in task.assigned_to.all():

            async_to_sync(channel_layer.group_send)(
                f"user_{employee.id}",
                {
                    "type": "task_updated",
                    "data": {
                        "task_id": task.id,
                        "status": task.status
                    }
                }
            )

        # New submission notification
        if submission_file:

            # Assigned employees
            for employee in task.assigned_to.all():

                async_to_sync(channel_layer.group_send)(
                    f"user_{employee.id}",
                    {
                        "type": "submission_uploaded",
                        "data": {
                            "task_id": task.id,
                            "file_name": submission_file.name,
                            "uploaded_by": self.request.user.username
                        }
                    }
                )

            # Task creator (manager/admin)
            async_to_sync(channel_layer.group_send)(
                f"user_{task.created_by.id}",
                {
                    "type": "submission_uploaded",
                    "data": {
                        "task_id": task.id,
                        "file_name": submission_file.name,
                        "uploaded_by": self.request.user.username
                    }
                }
            )
       


# Create Task Page
def create_task_page(request):
    return render(request, "create_task.html")


# Task Detail Page
def task_detail_page(request):    
   
    return render(request, "task_detail.html")



# Task Edit Page
def task_edit_page(request):
    return render(request, "task_edit.html")



# chat message view
class ChatMessageListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        task_id = request.GET.get("task")
        task = get_object_or_404(Task, id=task_id)

        messages = Message.objects.filter(
            task=task
        ).order_by("created_at")

        data = [
            {
                "sender_id": m.sender_id,
                "message": m.message,
            }
            for m in messages
        ]
        return Response(data)
    



# notification list api view
class NotificationListAPIView(ListAPIView):

    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user
        ).order_by("-created_at")[:8]



# notification count api view
class NotificationCountAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        count = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count()
        return Response({"count": count})
    

# mark nofitifiaction read 
class MarkNotificationReadAPIView(UpdateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def perform_update(self, serializer):
        serializer.save(is_read=True)




