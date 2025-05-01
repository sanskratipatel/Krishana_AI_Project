from django.urls import path
from .views import chatbot_api,user_dashboard, user_data, chat_history_api

urlpatterns = [
    path("chatbot/", chatbot_api, name="chatbot_api"),
    path("history/", chat_history_api, name="chat_history_api"),
    path("desktop/", user_dashboard, name="user_dashboard"),  # ✅ Route for Desktop Page
    path("user-data/", user_data, name="user_data"),
]
