from rest_framework import serializers
from api.models import Plant
  

class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = '__all__'