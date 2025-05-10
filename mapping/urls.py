from django.urls import path
from .views import ParkListCreateAPIView
from . import views

urlpatterns = [
    path('parks/', ParkListCreateAPIView.as_view(), name='park-list-create'),
    path('map/', views.map, name='map'),
    path('navbar/', views.navbar, name='navbar'),
]
