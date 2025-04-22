from django.db import models

class Plant(models.Model):
    common_name = models.CharField(max_length=255)
    scientific_name = models.CharField(max_length=255)
    category = models.CharField(max_length=255, blank=True, null=True)
    url = models.URLField()
    culinaryUse = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    humidityPreference = models.CharField(max_length=255, blank=True, null=True)
    life_span = models.CharField(max_length=255, blank=True, null=True)
    medicinalUses = models.TextField(blank=True, null=True)
    plant_Type = models.CharField(max_length=255, blank=True, null=True)
    sunlight = models.CharField(max_length=255, blank=True, null=True)
    wateringNeeds = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.common_name
