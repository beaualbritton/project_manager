# api/views/employees.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from ..models import Employee
from ..serializers import EmployeeListSerializer

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def get_employee(request):
    # 1. Try to get employeeID from the request body (request.data)
    # 2. If not there, try to get it from the URL parameters (request.query_params)
    employee_id = request.data.get('employeeID') or request.query_params.get('employeeID')

    # Start with the optimized queryset
    queryset = Employee.objects.all().select_related('user', 'company').prefetch_related('teams')

    # If an ID was provided, filter the list down to just that one
    if employee_id:
        queryset = queryset.filter(employeeID=employee_id)

    # By using many=True, DRF always returns a JSON array [] 
    # even if there is only one item or zero items.
    serializer = EmployeeListSerializer(queryset, many=True)
    
    return Response(serializer.data)
