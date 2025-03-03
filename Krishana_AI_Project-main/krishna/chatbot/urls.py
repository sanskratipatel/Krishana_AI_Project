from django.urls import path
from .views import get_mythology_answer

urlpatterns = [
    path("chat/ask/", get_mythology_answer, name="ask"),
]
