from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from ..models import Team
from ..serializers import TeamListSerializer

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
