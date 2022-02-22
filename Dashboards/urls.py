from django.contrib import admin
from django.urls import path
from . import views
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboardindex/', views.indexView, name="index"),

]