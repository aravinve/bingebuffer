from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('confirmation/', views.accounts_confirmation_view, name='confirmation'),
    path('signup/', views.signup_view, name='signup'),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]