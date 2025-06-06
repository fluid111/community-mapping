from rest_framework import serializers
from .models import Park

class ParkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Park
        fields = '__all__'

#  ModelSerializer's .create() or .update()
#  creation and update for add_park and edit_park 

