from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import ChatbotMessage

# Simple chatbot logic
def get_bot_response(user_message):
    responses = {
        "hello": "Hi there! How can I help you?",
        "how are you?": "I'm just a bot, but I'm doing great! How about you?",
        "bye": "Goodbye! Have a great day!",
        "who are you?": "I am your chatbot assistant!"
    }
    return responses.get(user_message.lower(), "Sorry, I don't understand that.")

@csrf_exempt  # Disable CSRF for testing
def chatbot_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Get user input from request
            user_message = data.get("message", "").strip()  # Get the message
            
            if not user_message:
                return JsonResponse({"error": "Message cannot be empty"}, status=400)
            
            bot_response = get_bot_response(user_message)  # Get chatbot response
            
            # Save the conversation in the database
            ChatbotMessage.objects.create(user_message=user_message, bot_response=bot_response)

            return JsonResponse({"response": bot_response})
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    return JsonResponse({"error": "Only POST requests are allowed"}, status=405)
