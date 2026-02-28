from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..models import Employee
from ..serializers import EmployeeListSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated]) # Ensures only logged-in users can see the list
def get_employee_list(request):
    """
    Returns a list of all employees in the database.
    """
    # Use select_related to optimize the database query (prevents N+1 problem)
    employees = Employee.objects.all().select_related('user', 'company')
    
    serializer = EmployeeListSerializer(employees, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
