"""
Core views for app.
"""

# from rest_framework import status # fix guess serializer
from drf_spectacular.utils import OpenApiResponse, extend_schema  # fix guess serializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


# this decorator is to fix guess serializer error
@extend_schema(
    responses={
        200: OpenApiResponse(
            description="API is healthy",
            response={'type': 'object', 'properties': {'healthy': {'type': 'boolean'}}}
        )
    }
)

@api_view(['GET'])
def health_check(request):
    """Returns successful response."""
    return Response({'healthy': True})
