from django.urls import path
from . import views

app_name = 'blogger'

urlpatterns = [
    path('', views.blogger_home, name='home'),
    path('page/<str:dataType>/<int:page>', views.blogger_page, name='page'),
    path('detail/<str:id>', views.blogger_detail, name='detail'),
]