# management/commands/import_plants.py
from django.core.management.base import BaseCommand
from api.models import Plant  # your model
from api.common.utils import fetch_convex_data

class Command(BaseCommand):
    help = "Import plant data from Convex API"

    def handle(self, *args, **kwargs):
        plants_data = fetch_convex_data()
        print("Parsed Plant Data:", plants_data)

        if isinstance(plants_data, dict):
            # If it's wrapped in a dict like {"plants": [...]}, extract it
            plants_data = plants_data.get("plants", [])

        for plant in plants_data:
            if isinstance(plant, dict):
                Plant.objects.create(
                    common_name=plant.get("common_name", ""),
                    scientific_name=plant.get("scientific_name", ""),
                    category=plant.get("category", ""),
                    url=plant.get("url", ""),
                    culinaryUse=plant.get("culinaryUse", ""),
                    description=plant.get("description", ""),
                    humidityPreference=plant.get("humidityPreference", ""),
                    life_span=plant.get("life_span", ""),
                    medicinalUses=plant.get("medicinalUses", ""),
                    plant_Type=plant.get("plant_Type", ""),
                    sunlight=plant.get("sunlight", ""),
                    wateringNeeds=plant.get("wateringNeeds", "")
                )

        self.stdout.write(self.style.SUCCESS("Successfully imported plants from Convex!"))