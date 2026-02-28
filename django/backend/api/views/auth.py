from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt

# alias
create_employee = Employee.objects.create_user


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
def register(request):
    
