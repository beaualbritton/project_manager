from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt

from .serializers import RegisterSerializer

@api_view(["GET"])
def check(request):
    return Response(status=200)

@api_view(["GET"])
# basic cookie
def csrf_token(request):
    return Response({"csrfToken": get_token(request)})

@api_view(["POST"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)

@api_view(["POST"])
@permission_classes([AllowAny]) # Allows access even if not logged in
def register(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "User and Employee profile created successfully."
        }, status=status.HTTP_201_CREATED)

    # If validation fails, return the specific errors (e.g., "Username already taken")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
