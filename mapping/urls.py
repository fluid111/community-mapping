from django.urls import path
from .views import ParkListCreateAPIView
from . import views

urlpatterns = [
    path('parks/', ParkListCreateAPIView.as_view(), name='park-list-create'),
    path('map/', views.map, name='map'),
    path('navbar/', views.location, name='navbar'),
    path('add-park/', views.add_park, name='add-park'),
    path('delete-park/<int:park_id>/', views.delete_park, name='delete-park'),

]
