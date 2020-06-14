from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('', views.booking_home, name='home'),
    path('search/', views.booking_search, name='search'),
    path('detail/<str:id>', views.booking_detail, name='detail'),
]