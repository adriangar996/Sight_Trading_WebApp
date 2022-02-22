from django.contrib import admin
from django.urls import path
from . import views
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homeView, name="landing"),
    path('login/', views.loginView, name="login"),
    path('signup/', views.signupView, name="signup"),
    path('logout/', views.logout_user, name="logout"),
]
