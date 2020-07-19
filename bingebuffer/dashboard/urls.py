from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('feed/', views.dashboard_feed, name='feed'),
    path('profile/', views.dashboard_profile, name='profile'),
    path('userprofile/', views.dashboard_userprofile, name='userprofile'),
    path('password/', views.dashboard_password, name='password'),
    path('bookings/', views.dashboard_bookings, name='bookings'),
    path('settings/', views.dashboard_settings, name='settings'),
    path('bookings/pdf/<str:id>', views.dashboard_ticket_pdf, name='pdf'),
    path('postreview/', views.dashboard_postreview, name='postreview'),
]