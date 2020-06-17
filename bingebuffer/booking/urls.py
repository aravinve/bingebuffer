from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('', views.booking_home, name='home'),
    path('page/<str:dataType>/<int:page>', views.booking_page, name='page'),
    path('detail/<str:id>', views.booking_detail, name='detail'),
    path('imdb/<str:id>', views.booking_imdb_detail, name='imdbdetail'),
    path('search/', views.booking_search, name='search_movie'),
    path('shows/<str:movieId>', views.booking_shows, name='shows'),
    path('seatselection/', views.booking_seat_selection, name='seats'),
]