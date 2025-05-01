from django.db import models
from django.contrib.auth.models import User

class ChatbotMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 🔑 Link to logged-in user
    user_message = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.user_message} => {self.bot_response}"

