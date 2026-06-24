from django.test import TestCase

# Create your tests here.
# tasks/tests.py
from django.test import TestCase
from .models import Task

class TaskModelTest(TestCase):
    def test_task_creation(self):
        task = Task.objects.create(
            title="Learn GitHub Actions"
        )

        self.assertEqual(task.title, "Learn GitHub Actions")