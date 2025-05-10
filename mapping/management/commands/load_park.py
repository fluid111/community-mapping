import json
from django.conf import settings
from django.core.management.base import BaseCommand
from mapping.models import Park

class Command(BaseCommand):
    help = 'Load park data from GeoJSON file'

    def handle(self, *args, **kwargs):
        data_file = settings.BASE_DIR / 'data' / 'park' / 'export.geojson'
        
        with open(data_file, 'r') as geofile:
            data = json.load(geofile)
            features = data['features']

        for feature in features:
            properties = feature['properties']
            geometry = feature['geometry']
            
            # Calculate centroid for the park's coordinates
            if geometry['type'] == 'Polygon':
                coordinates = geometry['coordinates'][0]  # Take the first ring
                num_points = len(coordinates)
                if num_points > 0:
                    avg_longitude = sum(coord[0] for coord in coordinates) / num_points
                    avg_latitude = sum(coord[1] for coord in coordinates) / num_points

                    # Add park to database
                    Park.objects.get_or_create(
                        name=properties.get('name', ''),
                        description=f"{properties.get('leisure', '')} - {properties.get('landuse', '')}",
                        latitude=avg_latitude,
                        longitude=avg_longitude
                    )

        self.stdout.write(self.style.SUCCESS('Successfully loaded park data'))