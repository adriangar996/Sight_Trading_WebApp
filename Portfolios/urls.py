from django.contrib import admin
from django.urls import path
from . import views
from django.urls import path, include

app_name = "Portfolios"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('portfolio/', views.portfolioView, name="portfolio"),
    path('watchlist/', views.watchlistView, name="watchlist"),
    path('notifications/', views.notificationsView, name="notifications"),
    path('settings/', views.settingsView, name="settings"),
    path('help/', views.helpView, name="help"),
    path('theme/', views.theme, name="theme"),

]