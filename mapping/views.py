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
    context={'park':park}
    return render(request, 'mapping/index.html', context)


def location(request):
    # parks = Park.objects.values('id','latitude', 'longitude')[:100]
    parks = Park.objects.values('name', 'id','latitude', 'longitude')
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

# @csrf_exempt
@api_view(['PUT'])
def edit_park(request, park_id):
    if request.method == 'PUT':
        try:
            park = Park.objects.get(id=park_id)

            newlatitude = request.data.get('latitude')
            newlongitude = request.data.get('longitude')

            if newlatitude is None or newlongitude is None:
             return Response({'error': 'Missing coordinates'}, status=status.HTTP_400_BAD_REQUEST)

            park.latitude = newlatitude
            park.longitude = newlongitude
            park.save()

            return Response({'park id received'}, status=status.HTTP_200_OK)
        
        except Park.DoesNotExist:
         return Response({'error': 'Park not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"An exception occurred: {e}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
def map(request):
    return render(request, 'mapping/map.html')
