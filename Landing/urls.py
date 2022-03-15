from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "Landing"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homeView, name="landing"),
    path('landing/', views.homeView, name="landing"),
    path('login/', views.loginView, name="login"),
    path('signup/', views.signupView, name="signup"),
    path('logout/', views.logout_user, name="logout"),
    path('password_reset/', views.password_reset_request, name="password_reset"),
    path('password_reset_complete/', views.password_reset_complete, name="password_reset_complete"),
]
