from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Ensure email is unique
    username = models.CharField(max_length=150, blank=True, null=True)

    USERNAME_FIELD = "email"  # Use email instead of username
    REQUIRED_FIELDS = []  # No additional required fields

    def __str__(self):
        return self.email
