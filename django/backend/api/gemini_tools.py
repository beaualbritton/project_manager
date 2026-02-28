from .models import Task, Employee, Team, SubTask
from .serializers import EmployeeListSerializer, TeamListSerializer
from django.db.models import Q

# Define functions that match your endpoint logic
def get_from_username(employee_name: str):
    try:
        # We search across username, first name, and last name (case-insensitive)
        employee = Employee.objects.filter(
            Q(user__username__icontains=employee_name) |
            Q(user__first_name__icontains=employee_name) |
            Q(user__last_name__icontains=employee_name)
        ).first()

        if employee:
            return str(employee.employeeID)
        return "Employee not found."
    except Exception as e:
        return f"Error: {str(e)}"

def list_tasks(employee_id: str):
    """Retrieves all tasks and subtasks for a specific employee's teams."""
    try:
        employee = Employee.objects.get(employeeID=employee_id)
        tasks = Task.objects.filter(team__in=employee.teams.all()).prefetch_related("subtasks")
        return [
            {
                "name": t.name, 
                "status": t.status, 
                "subtasks": [s.name for s in t.subtasks.all()]
            } for t in tasks
        ]
    except Exception as e:
        return f"Error: {str(e)}"

def create_new_task(name: str, team_id: str, budget: str):
    """Creates a new task for a specific team."""
    try:
        team = Team.objects.get(teamID=team_id)
        task = Task.objects.create(name=name, team=team, budget=budget)
        return f"Successfully created task {name} with ID {task.taskID}"
    except Exception as e:
        return f"Error: {str(e)}"

def list_teams():
    """Returns a list of all teams and their leaders."""
    teams = Team.objects.all().select_related('leader')
    return [{"teamID": str(t.teamID), "name": t.name, "leader": t.leader.user.username} for t in teams]

# Add all tools to a list
AVAILABLE_TOOLS = [list_tasks, create_new_task, list_teams]