from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from ..models import Team, Employee
from ..serializers import TeamListSerializer, TeamCreateSerializer # Import both

@api_view(['POST'])
@permission_classes([AllowAny])
def add_team(request):
    """
    Creates a new team.
    Expected JSON: { "Name": "Backend Core", "compID": "uuid", "leaderID": "uuid" }
    """
    serializer = TeamCreateSerializer(data=request.data)
    
    if serializer.is_valid():
        new_team = serializer.save()
        
        # We use the ListSerializer for the response so the returned 
        # data matches your specific JSON format exactly.
        return Response(
            TeamListSerializer(new_team).data, 
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def add_employee(request):
    """
    Adds an existing employee to an existing team.
    Expected JSON: { "employeeID": "uuid", "teamID": "uuid" }
    """
    emp_id = request.data.get('employeeID')
    team_id = request.data.get('teamID')

    if not emp_id or not team_id:
        return Response(
            {"error": "Both employeeID and teamID are required."}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Look up both entities
        employee = Employee.objects.get(employeeID=emp_id)
        team = Team.objects.get(teamID=team_id)

        # Use the .add() method for the ManyToMany relationship
        # This populates the api_employee_teams table
        employee.teams.add(team)

        return Response({
            "message": f"Employee {employee.user.username} successfully added to team {team.name}."
        }, status=status.HTTP_200_OK)

    except Employee.DoesNotExist:
        return Response({"error": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)
    except Team.DoesNotExist:
        return Response({"error": "Team not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def get_team(request):
    """
    Returns a list of teams. 
    If teamID is in the request body/params, returns a list with one team.
    Otherwise, returns all teams.
    """
    # Look for teamID in body (data) or URL parameters (query_params)
    team_id = request.data.get('teamID') or request.query_params.get('teamID')

    # Optimization: prefetch_related('tasks') prevents N+1 queries for task lists
    # select_related('company', 'leader') prevents N+1 queries for company/leader IDs
    queryset = Team.objects.all().select_related('company', 'leader').prefetch_related('tasks')

    if team_id:
        queryset = queryset.filter(teamID=team_id)

    serializer = TeamListSerializer(queryset, many=True)
    return Response(serializer.data)
