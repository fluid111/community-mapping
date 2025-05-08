from django.urls import path
from .views import ParkListCreateAPIView

urlpatterns = [
    path('parks/', ParkListCreateAPIView.as_view(), name='park-list-create'),
]
