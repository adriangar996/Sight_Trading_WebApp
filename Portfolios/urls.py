from django.contrib import admin
from django.urls import path
from . import views
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('portfolio/', views.portfolioView, name="portfolio"),

]