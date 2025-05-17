from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.utils.timezone import now, timedelta
from django.contrib import messages
from .models import CustomUser 
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth.models import User
from users.models import CustomUser
import random
from django.contrib.auth import login
from django.contrib.auth import get_user_model


# Home Page View
def home_view(request):
    return render(request, "home.html")


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email").strip()
        password = request.POST.get("password").strip()

        # ✅ Check if email exists in the database
        try:
            user = CustomUser.objects.get(email=email)

            # ✅ Authenticate using email as username
            user_authenticated = authenticate(request, email=email, password=password)

            # ✅ Check if password is correct
            if user_authenticated:
                login(request, user_authenticated)
                messages.success(request, "Login successful!")
                return redirect("dashboard")
            else:
                # ✅ Email exists but the password is incorrect
                messages.error(request, "Your password is wrong. Please try again.")
        
        except CustomUser.DoesNotExist:
            # ✅ If email does not exist, show this message
            messages.error(request, "Email does not exist. Please sign up first.")

    return render(request, "login.html")

 


User = get_user_model()

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username").strip()
        email = request.POST.get("email").strip()
        password1 = request.POST.get("password1").strip()
        password2 = request.POST.get("password2").strip()

        # ✅ Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "This email already exists. Please login.")
            return redirect('login')

        # ✅ Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "This username is already taken. Try a different one.")
            return redirect('signup')

        # ✅ Check if both passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        otp = generate_otp()

        # ✅ Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            otp=otp
        )
        user.save()

        send_mail(
            'Your OTP Code for Account Verification',
            f'Your OTP Code is: {otp}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        # ✅ Set authentication backend explicitly
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        messages.success(request, "Account created successfully!")
        return redirect(reverse('verify-otp', kwargs={'email': email}))

    return render(request, "signup.html")



# OTP Verification View
def verify_otp(request, email):
    if request.method == "POST":
        otp_entered = request.POST.get("otp")
        user = CustomUser.objects.get(email=email)

        if user.otp == otp_entered:
            user.is_email_verified = True
            user.save()
            login(request, user)
            messages.success(request, "Account verified successfully!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect(reverse('verify-otp', kwargs={'email': email}))
    return render(request, "verify_otp.html", {'email': email})


def google_login(request):
    return redirect("/accounts/google/login")


# ✅ GitHub OAuth Login
def github_login(request):
    return redirect("/accounts/github/login") 


# # Forgot Password View
# def forgot_password_view(request):
#     return render(request, "forgot_password.html")

# Dashboard View
def dashboard_view(request):
    return render(request, "dashboard.html")

otp_attempts = {}  # Dictionary to track OTP attempts for each email



# ✅ Generate OTP with Expiry
def generate_otp():
    return str(random.randint(100000, 999999))

# ✅ Forget Password - Step 1 (Send OTP)
def forget_password_view(request):
    if request.method == "POST":
        email = request.POST.get("email").strip()

        try:
            user = CustomUser.objects.get(email=email)
            otp = generate_otp()
            user.otp = otp
            user.otp_expiry = now() + timedelta(minutes=5)  # OTP valid for 5 minutes
            user.save()

            send_mail(
                'Your OTP for Password Reset',
                f'Your OTP Code is: {otp}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            otp_attempts[email] = 0  # Reset OTP attempts
            messages.success(request, "OTP has been sent to your email.")
            return redirect(reverse('verify-forgot-otp', kwargs={'email': email}))

        except CustomUser.DoesNotExist:
            messages.error(request, "This email is not registered.")
    
    return render(request, "forget_password.html")

# ✅ Verify OTP - Step 2
def verify_forgot_otp(request, email):
    if request.method == "POST":
        otp_entered = request.POST.get("otp")
        
        try:
            user = CustomUser.objects.get(email=email)

            # ✅ Check if OTP matches and is within expiry time
            if user.otp == otp_entered and user.otp_expiry > now():
                messages.success(request, "OTP Verified! You can now reset your password.")
                return redirect(reverse('change-password', kwargs={'email': email}))
            else:
                messages.error(request, "Invalid or expired OTP.")
                return redirect(reverse('verify-forgot-otp', kwargs={'email': email}))

        except CustomUser.DoesNotExist:
            messages.error(request, "Invalid request.")

    return render(request, "verify_forgot_otp.html", {'email': email})

# ✅ Reset Password - Step 3
def change_password_view(request, email):
    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect(reverse('change-password', kwargs={'email': email}))

        user = CustomUser.objects.get(email=email)
        user.set_password(new_password)
        user.otp = None  # Clear OTP after use
        user.save()

        messages.success(request, "Password changed successfully! You can now log in.")
        return redirect('login')

    return render(request, "change-password.html", {'email': email})



# # ✅ Forget Password View - Step 1 (Enter Email)
# def forget_password_view(request):
#     if request.method == "POST":
#         email = request.POST.get("email").strip()

#         try:
#             user = CustomUser.objects.get(email=email)
#             otp = generate_otp()
#             user.otp = otp
#             user.save()

#             send_mail(
#                 'Your OTP for Password Reset',
#                 f'Your OTP Code is: {otp}',
#                 settings.EMAIL_HOST_USER,
#                 [email],
#                 fail_silently=False,
#             )

#             otp_attempts[email] = 0  # Reset OTP attempts
#             messages.success(request, "OTP has been sent to your email.")
#             return redirect(reverse('verify-forgot-otp', kwargs={'email': email}))

#         except CustomUser.DoesNotExist:
#             messages.error(request, "This email is not registered.")
    
#     return render(request, "forget_password.html")

# # ✅ Verify OTP View - Step 2 (Enter OTP)
# def verify_forgot_otp(request, email):
#     global otp_attempts

#     if request.method == "POST":
#         otp_entered = request.POST.get("otp")
#         user = CustomUser.objects.get(email=email)

#         if user.otp == otp_entered:
#             messages.success(request, "OTP Verified! You can now reset your password.")
#             return redirect(reverse('change-password', kwargs={'email': email}))

#         otp_attempts[email] += 1
#         if otp_attempts[email] >= 3:
#             messages.error(request, "Too many failed attempts. Resend OTP.")
#             return redirect(reverse('forget-password'))
        
#         messages.error(request, f"Invalid OTP. {3 - otp_attempts[email]} attempts left.")
    
#     return render(request, "verify_forgot_otp.html", {'email': email})

# # ✅ Change Password View - Step 3 (Enter New Password)
# def change_password_view(request, email):
#     if request.method == "POST":
#         new_password = request.POST.get("new_password")
#         confirm_password = request.POST.get("confirm_password")

#         if new_password != confirm_password:
#             messages.error(request, "Passwords do not match.")
#             return redirect(reverse('change-password', kwargs={'email': email}))

#         user = CustomUser.objects.get(email=email)
#         user.set_password(new_password)
#         user.save()

#         messages.success(request, "Password changed successfully! You can now login.")
#         return redirect('login')

#     return render(request, "change-password.html", {'email': email}) 


