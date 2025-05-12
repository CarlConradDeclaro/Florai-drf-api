
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.serializers import PlantSerializer
from api.models import Plant
from api.common.services.embeddings import semantic_search


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def plant_info(request):
    plants = Plant.objects.all()
    serializer = PlantSerializer(plants,many=True)
    return Response(serializer.data)



@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def semantic_search_view(request):
    query = request.query_params.get("q", "")
    if not query:
        return Response({"error": "Query parameter 'q' is required."}, status=400)

    plants = Plant.objects.all()
    descriptions = [plant.description or "" for plant in plants]

    indices, _ = semantic_search(query, descriptions)

    # Convert indices to standard Python integers
    indices = [int(i) for i in indices]

    matched_plants = [plants[i] for i in indices]

    serializer = PlantSerializer(matched_plants, many=True)
    return Response(serializer.data)
 
 


