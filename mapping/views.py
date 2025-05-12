from rest_framework import generics
from .models import Park
from .serializers import ParkSerializer
from django.http import JsonResponse

from rest_framework.decorators import api_view

from django.shortcuts import render

class ParkListCreateAPIView(generics.ListCreateAPIView):
    queryset = Park.objects.all()
    serializer_class = ParkSerializer

    def get_queryset(self):
        return Park.objects.all()

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

# @csrf_exempt  # Temporarily disable CSRF for simplicity (use proper CSRF handling in production)
@api_view(['POST'])
def add_park(request):
    if request.method == 'POST':
        try:
            data = request.data  # Use request.data since it's a DRF view
            latitude = data.get('latitude')
            longitude = data.get('longitude')

            if latitude is None or longitude is None:
                return JsonResponse({'error': 'Latitude and longitude are required'}, status=400)

            if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
                return JsonResponse({'error': 'Invalid coordinates'}, status=400)

            park = Park.objects.create(
                name=f"Park at {latitude}, {longitude}",
                latitude=latitude,
                longitude=longitude
            )
            return JsonResponse({'message': 'Park added successfully', 'id': park.id}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
def map(request):
    return render(request, 'mapping/map.html')
# def navbar(request):
#     return render(request, 'mapping/index.html')