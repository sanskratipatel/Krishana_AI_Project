
from django.db import models

class ChatbotMessage(models.Model):
    user_message = models.TextField()  # Stores the user's message
    bot_response = models.TextField()  # Stores the chatbot's response
    timestamp = models.DateTimeField(auto_now_add=True)  # Auto timestamp

    def __str__(self):
        return f"User: {self.user_message} | Bot: {self.bot_response}"
