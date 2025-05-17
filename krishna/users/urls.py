# from django.urls import path
# from .views import home_view, login_view, signup_view

# urlpatterns = [
#     path('', home_view, name='home'),
#     path('login/', login_view, name='login'),
#     # path('signup/', views.signup, name='signup'),
#     # path('logout/', views.logout_view, name='logout'),
# ]   


from django.urls import path
from .views import home_view, login_view, signup_view, dashboard_view
from .views import forget_password_view, verify_forgot_otp, change_password_view
from .views import signup_view, login_view, verify_otp, google_login, github_login
# from .views import forgot_password_view, verify_forgot_otp, reset_password
urlpatterns = [
    path('', home_view, name='home'),
    path('home/', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('verify-otp/<str:email>/', verify_otp, name='verify-otp'),
    path('google-login/', google_login, name='google-login'),
    path('github-login/', github_login, name='github-login'),
    path('signup/', signup_view, name='signup'),
    path("dashboard/", dashboard_view, name="dashboard"),
    path('forgot-password/', forget_password_view, name='forget_password'),
    path('verify-forgot-otp/<str:email>/', verify_forgot_otp, name='verify-forgot-otp'),
    path('change-password/<str:email>/', change_password_view, name='change-password'),
]
 