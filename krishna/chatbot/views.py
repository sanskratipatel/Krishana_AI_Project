from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from langdetect import detect
from .models import ChatbotMessage
import random
import openai
from django.conf import settings


def get_bot_response(user_message, language="en"):
    openai.api_key = settings.OPENAI_API_KEY
    prompt = f"You are Krishna AI Assistant. Answer in {language}.\nUser: {message}\nAI:"
    response = openai.Completion.create(
        engine="text-davinci-003",  # Or "gpt-3.5-turbo" if using Chat API
        prompt=prompt,
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].text.strip()

# Simple chatbot logic
@login_required
def user_dashboard(request):
    """Redirects users to their respective dashboards"""
    return render(request, "chatbot/user_dashboard.html")

@csrf_exempt
@login_required
def chatbot_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "").strip()
            language = data.get("language", "en")  # Default to English

            if not user_message:
                return JsonResponse({"error": "Message cannot be empty"}, status=400)

            bot_response = get_bot_response(user_message, language)

            # Store chat history
            ChatbotMessage.objects.create(
                user=request.user,
                user_message=user_message,
                bot_response=bot_response)
            return JsonResponse({"response": bot_response})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Only POST requests allowed"}, status=405)




@csrf_exempt
def chat_history_api(request):
    search_query = request.GET.get("q", "")
    if search_query:
        history = ChatbotMessage.objects.filter(user=request.user, user_message__icontains=search_query)
    else:
        history = ChatbotMessage.objects.filter(user=request.user).order_by("-timestamp")[:20]

    data = [{"question": m.user_message, "answer": m.bot_response, "time": m.timestamp} for m in history]
    return JsonResponse({"history": data})


@login_required
def user_data(request):
    return JsonResponse({"username": request.user.username})

@login_required
def chat_history(request):
    search_query = request.GET.get("q", "")
    page = int(request.GET.get("page", 1))

    history_qs = ChatbotMessage.objects.filter(user=request.user)
    if search_query:
        history_qs = history_qs.filter(user_message__icontains=search_query)

    history_qs = history_qs.order_by("-timestamp")
    paginator = Paginator(history_qs, 10)  # 10 per page
    page_obj = paginator.get_page(page)

    data = [{
        "question": m.user_message,
        "answer": m.bot_response,
        "time": m.timestamp
    } for m in page_obj]

    return JsonResponse({"history": data, "has_more": page_obj.has_next()})

