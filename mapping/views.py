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
    park=Park.objects.values('latitude','longitude')[:100]
    print(park[:2])
    context={'park':park}
    return render(request, 'mapping/index.html', context)

# def location(request):
#     point = list(Park.objects.values('latitude','longitude')[:100])
#     print(point[:2])
#     context = {'point':point}
#     return render (request, 'mapping/index.html', context)

def location(request):
    # Fetch parks and filter out invalid coordinates
    parks = Park.objects.values('latitude', 'longitude')[:100]
    point = [
        park for park in parks
        if park['latitude'] is not None and park['longitude'] is not None
        and -90 <= park['latitude'] <= 90
        and -180 <= park['longitude'] <= 180
    ]
    print("location view - First two parks:", point[:2])
    context = {'point': point}
    return render(request, 'mapping/index.html', context)

def map(request):
    return render(request, 'mapping/map.html')
# def navbar(request):
#     return render(request, 'mapping/index.html')