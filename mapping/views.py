from rest_framework import generics
from .models import Park
from .serializers import ParkSerializer

from rest_framework.decorators import api_view

from django.shortcuts import render

class ParkListCreateAPIView(generics.ListCreateAPIView):
    queryset = Park.objects.all()
    serializer_class = ParkSerializer

@api_view(['GET'])
def park_locations(request):
    park=Park.objects.value('latitdue','longitude')[:100]
    print(park)
    context={'park':park}
    return render(request, 'map.html', context)

def map(request):
    return render(request, 'mapping/map.html')
def navbar(request):
    return render(request, 'mapping/index.html')