from rest_framework import generics
from .models import Park
from .serializers import ParkSerializer

class ParkListCreateAPIView(generics.ListCreateAPIView):
    queryset = Park.objects.all()
    serializer_class = ParkSerializer
