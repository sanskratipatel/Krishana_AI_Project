
# from django.shortcuts import render, redirect
# from django.contrib.auth import login, authenticate
# from django.contrib.auth.forms import UserCreationForm
# from .models import CustomUser

# def login_view(request):
#     if request.method == "POST":
#         email = request.POST["email"]
#         password = request.POST["password"]
#         user = authenticate(request, username=email, password=password)
#         if user:
#             login(request, user)
#             return redirect("/")
#     return render(request, "login.html")

# def signup_view(request):
#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.username = user.email  # Set username as email
#             user.save()
#             login(request, user)
#             return redirect("/")
#     else:
#         form = UserCreationForm()
#     return render(request, "signup.html", {"form": form})
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import CustomUser, ChatbotMessage # Ensure you have a CustomUser model if using a custom user model

# Home Page View
def home_view(request):
    return render(request, "home.html")  # Renders home.html as the welcome page

# Login View
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")  # Using .get() for safety
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect("home")  # Redirects to home page after login
    return render(request, "login.html")

# Signup View
def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email  # Ensures username is set to email
            user.save()
            login(request, user)
            return redirect("user_dashboard.html")  # Redirects to home page after signup
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form})


