from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('feed/', views.dashboard_feed, name='feed'),
    path('profile/', views.dashboard_profile, name='profile'),
    path('bookings/', views.dashboard_bookings, name='bookings'),
    path('settings/', views.dashboard_settings, name='settings'),
]