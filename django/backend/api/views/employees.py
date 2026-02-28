# api/views/employees.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from ..models import Employee
from ..serializers import EmployeeListSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def get_employee_list(request):
    # select_related for 1-to-1/ForeignKeys, prefetch_related for ManyToMany
    employees = Employee.objects.all().select_related('user', 'company').prefetch_related('teams')
    
    serializer = EmployeeListSerializer(employees, many=True)
    return Response(serializer.data)
