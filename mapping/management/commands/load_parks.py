import json
import codecs
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from mapping.models import Park


class Command(BaseCommand):
    help = 'Load park data from GeoJSON file'

    def handle(self, *args, **kwargs):
        # Update path to match your actual file location
        data_file = settings.BASE_DIR / 'data' / 'park' / 'parks.geojson'
        
        # Debug output
        self.stdout.write(f"Looking for file at: {data_file}")
        
        try:
            # Read the file in binary mode first
            with open(data_file, 'rb') as binary_file:
                binary_content = binary_file.read()
                
            # Try to detect encoding
            encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
            content = None
            
            for encoding in encodings:
                try:
                    self.stdout.write(f"Trying encoding: {encoding}")
                    content = binary_content.decode(encoding)
                    self.stdout.write(f"Successfully decoded with {encoding}")
                    break
                except UnicodeDecodeError:
                    self.stdout.write(f"Failed with {encoding}")
            
            if content is None:
                # If all encodings fail, try a more aggressive approach
                self.stdout.write("Trying to decode with errors='replace'")
                content = binary_content.decode('utf-8', errors='replace')
            
            # Parse the JSON
            data = json.loads(content)
            
            features = data.get('features', [])
            created_count = 0
            
            self.stdout.write(f"Found {len(features)} features in the GeoJSON file")
            
            for feature in features:
                # Skip features that aren't parks
                properties = feature.get('properties', {})
                if properties.get('leisure') != 'park':
                    continue
                    
                park_name = properties.get('name', '')
                
                # Get the geometry data
                geometry = feature.get('geometry', {})
                if geometry.get('type') == 'Polygon':
                    # For polygons, we'll use the first coordinate as the reference point
                    coordinates = geometry.get('coordinates', [])
                    if coordinates and coordinates[0]:
                        # GeoJSON format is [longitude, latitude]
                        longitude, latitude = coordinates[0][0]
                        
                        # Create or update park record
                        park, created = Park.objects.get_or_create(
                            name=park_name,
                            defaults={
                                'latitude': latitude,
                                'longitude': longitude,
                                'description': f"Park imported from OpenStreetMap data (ID: {properties.get('@id', 'unknown')})",
                                'created_at': timezone.now(),  # Explicitly set for clarity
                            }
                        )
                        
                        if not created:
                            # Update existing park with new coordinates
                            park.latitude = latitude
                            park.longitude = longitude
                            park.save()  # updated_at will be set automatically due to auto_now=True
                        
                        created_count += 1
                        self.stdout.write(f"Processed park: {park_name}")
            
            self.stdout.write(self.style.SUCCESS(f"Successfully imported {created_count} parks"))
            
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File not found: {data_file}"))
            self.stdout.write("Make sure your GeoJSON file is in the correct location")
            
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f"Error decoding JSON from the file: {str(e)}"))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))