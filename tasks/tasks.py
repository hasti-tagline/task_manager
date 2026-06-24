from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Task
from django.utils.timezone import localdate



# send assigned task email
@shared_task
def send_task_email(task_id):

    task = Task.objects.get(id=task_id)
    employees = task.assigned_to.all()
    for employee in employees:
        send_mail(
            subject="New Task Assigned",
            message=f"""
                Hello {employee.username},
                You have been assigned a new task.
                Title: {task.title}
                Description: {task.description}
                Due Date: {task.due_date}
                Status: {task.status}
                Priority: {task.priority}
                """,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[employee.email],
            fail_silently=False
        )



# pending and inprogress task daily reminder
@shared_task
def daily_task_reminder():

    tasks = Task.objects.filter(status__in=["pending","in_progress"])
    for task in tasks:
        employees = task.assigned_to.all()
        for employee in employees:
            send_mail(
                subject="Pending Task Reminder",
                message=f"""
                        Hello {employee.username},
                        Reminder for your task.
                        Title: {task.title}
                        Status: {task.status}
                        Priority: {task.priority}
                        Due Date: {task.due_date}
                        """,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[employee.email],
                fail_silently=False
            )




# automatically marks task as overdue 
@shared_task
def mark_overdue_tasks():

    tasks = Task.objects.filter(due_date__lte=localdate(),status__in=["pending", "in_progress", "review"])

    # change status to overdue
    for task in tasks:
        task.status = "overdue"
        task.save()

        # send mail to employees
        for employee in task.assigned_to.all():
            send_mail(
                subject="Task Overdue Alert",
                message=f"""
                    Hello {employee.username},
                    Your task "{task.title}" is now overdue.
                    Please complete it as soon as possible.
                    Due Date: {task.due_date}
                    Priority: {task.priority}
                    """,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[employee.email],
                fail_silently=False
            )