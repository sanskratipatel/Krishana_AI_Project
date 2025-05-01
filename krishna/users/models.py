from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Ensure email is unique
    username = models.CharField(max_length=150, blank=True, null=True)

    USERNAME_FIELD = "email"  # Use email instead of username
    REQUIRED_FIELDS = []  # No additional required fields

    def __str__(self):
        return self.email
    
class ChatbotMessage(models.Model):
    user_message = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.user_message} | Bot: {self.bot_response}"
