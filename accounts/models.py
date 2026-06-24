from django.contrib.auth.models import AbstractUser
from django.db import models
import secrets
from .utils import encrypt_api_key


def generate_api_key():
    raw_key = secrets.token_urlsafe(32)
    return encrypt_api_key(raw_key)


class User(AbstractUser):

    ROLE_CHOICES = (
        ("manager", "Manager"),
        ("employee", "Employee"),
        ("admin", "Admin"),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="employee"
    )

    api_key = models.TextField(
        unique=True,
        default=generate_api_key
    )   

    def __str__(self):

        return self.username
    
