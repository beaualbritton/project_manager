from django.contrib.auth import authenticate, login as django_login
from django.middleware.csrf import get_token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .serializers import RegisterSerializer

@api_view(["GET"])
def check(request):
    return Response({"message": "Authenticated", "user": request.user.username}, status=200)

@api_view(["GET"])
@permission_classes([AllowAny])
def csrf_token(request):
    # This manually sets the CSRF cookie and returns the token
    return Response({"csrfToken": get_token(request)})

@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    # 1. Verify credentials
    user = authenticate(username=username, password=password)
    if user is not None:
        # 2. Establish the session
        # This is required for session-based auth and CSRF rotation
        django_login(request, user)

        # 4. Access the Employee profile linked to this user
        employee = user.employee_profile
        return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "User and Employee profile created successfully."
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
