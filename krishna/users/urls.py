from django.urls import path
from .views import home_view, login_view,signup_view

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    # path('signup/', views.signup, name='signup'),
    # path('logout/', views.logout_view, name='logout'),
]
