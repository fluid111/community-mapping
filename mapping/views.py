import json
from rest_framework import generics
from .models import Park
from .serializers import ParkSerializer
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import api_view

from django.shortcuts import render

class ParkListCreateAPIView(generics.ListCreateAPIView):
    queryset = Park.objects.all()
    serializer_class = ParkSerializer

    def get_queryset(self):
        return Park.objects.all()

@api_view(['GET'])
def park_locations(request):
    park=Park.objects.values('latitude','longitude')
    # park=Park.objects.values('latitude','longitude')[:100]
    # print(park[:2])
    context={'park':park}
    return render(request, 'mapping/index.html', context)

# def location(request):
#     point = list(Park.objects.values('latitude','longitude')[:100])
#     print(point[:2])
#     context = {'point':point}
#     return render (request, 'mapping/index.html', context)
def location(request):
    # parks = Park.objects.values('id','latitude', 'longitude')[:100]
    parks = Park.objects.values('id','latitude', 'longitude')
    point = [
        park for park in parks
        if park['latitude'] is not None and park['longitude'] is not None
        and -90 <= park['latitude'] <= 90
        and -180 <= park['longitude'] <= 180
    ]
    # print("location view - First two parks:", point[:2])
    context = {'point': point}
    return render(request, 'mapping/index.html', context)

# @csrf_exempt  # Temporarily disable CSRF for simplicity (use proper CSRF handling in production)
@api_view(['POST'])
def add_park(request):
    if request.method == 'POST':
        try:
            # data = request.data  # Use request.data since it's a DRF view
            data = json.loads(request.body)
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            # park = Marker.objects.create(latitude=lat, longitude=lng)

            # if latitude is None or longitude is None:
            #     return JsonResponse({'error': 'Latitude and longitude are required'}, status=400)

            # try:
            #     latitude = float(latitude)
            #     longitude = float(longitude)
            # except ValueError:
            #     return Response({'error': 'Latitude and longitude must be valid numbers'}, status=status.HTTP_400_BAD_REQUEST)

            # if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
            #     return JsonResponse({'error': 'Invalid coordinates'}, status=400)

            park = Park.objects.create(
                name=f"Park at {latitude}, {longitude}",
                latitude=latitude,
                longitude=longitude
            )
            return JsonResponse({'message': 'Park added successfully', 'id': park.id}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    # return JsonResponse({'error': 'Invalid request method'}, status=405)

@api_view(['DELETE'])
def delete_park(request, park_id):
    if request.method == 'DELETE':
        try:
            park = Park.objects.get(id=park_id)
            park.delete()
            return Response({'message': 'Park deleted successfully'}, status=status.HTTP_200_OK)
        except Park.DoesNotExist:
            return Response({'error': 'Park not found'}, status=status.HTTP_404_NOT_FOUND)
    return JsonResponse({'error': 'Invalid method'}, status=400)

# def remove_marker(request):
#     if request.method =="POST":
#     # try:
#         parks = Park.objects.values('latitude', 'longitude')
def map(request):
    return render(request, 'mapping/map.html')
# def navbar(request):
#     return render(request, 'mapping/index.html')