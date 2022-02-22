from django.contrib import admin
from django.urls import path
from . import views
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('portfolio/', views.portfolioView, name="portfolio"),
    path('watchlist/', views.watchlistView, name="watchlist"),
    path('notifications/', views.notificationsView, name="notifications"),
    path('account/', views.accountView, name="account"),
    path('settings/', views.settingsView, name="settings"),
    path('help/', views.helpView, name="help"),

]