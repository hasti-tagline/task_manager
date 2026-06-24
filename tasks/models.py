from django.db import models
from django.conf import settings
from accounts.models import User

class Task(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("review", "Review"),
        ("rejected", "Rejected"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
        ("overdue","Overdue")
    ]

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("critical", "Critical"),
    ]

    title = models.CharField(max_length=255)

    description = models.TextField()

    assigned_to = models.ManyToManyField(User)

    created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="created_tasks",null=True,blank=True)

    due_date = models.DateField(null=True, blank=True)

    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default="pending")

    priority = models.CharField(max_length=20,choices=PRIORITY_CHOICES,default="medium")
    
    attachment = models.FileField(upload_to="task_files/",null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    submission = models.FileField(upload_to="task_files/",null=True,blank=True)



# notification class
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    task = models.ForeignKey(Task,on_delete=models.CASCADE,null=True,blank=True)



# message class
class Message(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE,null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
