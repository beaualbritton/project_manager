from .models import Task, Employee, Team, SubTask
from .serializers import EmployeeListSerializer, TeamListSerializer

# Define functions that match your endpoint logic
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