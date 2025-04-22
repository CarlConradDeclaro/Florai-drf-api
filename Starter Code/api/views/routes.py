
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


# Get All Routes
@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/plants/',
        '/plants/search/',
        '/api/token/',
        '/api/register/',
        '/api/token/refresh/'
    ]
    return Response(routes)
