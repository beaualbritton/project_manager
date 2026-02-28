from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Task, Employee, Team, SubTask


@api_view(["POST"])
def add_task(request):
    try:
        team = Team.objects.get(teamID=request.data.get("team_id"))
    except Team.DoesNotExist:
        return Response({"error": "Team not found"}, status=status.HTTP_404_NOT_FOUND)

    task = Task.objects.create(
        name=request.data.get("name"),
        start_date=request.data.get("start_date"),
        end_date=request.data.get("end_date"),
        budget=request.data.get("budget"),
        status=request.data.get("status", "ACTIVE"),
        team=team,
    )
    return Response({"message": "Task created", "taskID": str(task.taskID)}, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def get_tasks(request):
    employee_id = request.query_params.get("employee_id")

    try:
        employee = Employee.objects.get(employeeID=employee_id) if employee_id else request.user.employee_profile
    except Employee.DoesNotExist:
        return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

    tasks = Task.objects.filter(team__in=employee.teams.all()).prefetch_related("subtasks")

    return Response({
        "tasks": [
            {
                "taskID": str(t.taskID),
                "name": t.name,
                "start_date": t.start_date,
                "end_date": t.end_date,
                "budget": str(t.budget),
                "status": t.status,
                "teamID": str(t.team.teamID),
                "subtasks": [
                    {"subtaskID": str(s.subtaskID), "name": s.name, "status": s.status}
                    for s in t.subtasks.all()
                ],
            }
            for t in tasks
        ]
    }, status=status.HTTP_200_OK)


@api_view(["POST"])
def delete_task(request):
    try:
        task = Task.objects.get(taskID=request.data.get("task_id"))
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

    task.delete()
    return Response({"message": "Task deleted"}, status=status.HTTP_200_OK)


@api_view(["POST"])
def remove_task_from(request):
    try:
        task = Task.objects.get(taskID=request.data.get("task_id"))
        employee = Employee.objects.get(employeeID=request.data.get("employee_id"))
    except (Task.DoesNotExist, Employee.DoesNotExist) as e:
        return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    employee.teams.remove(task.team)
    return Response({"message": "Employee removed from task's team"}, status=status.HTTP_200_OK)


@api_view(["POST"])
def add_subtask(request):
    try:
        task = Task.objects.get(taskID=request.data.get("task_id"))
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

    subtask = SubTask.objects.create(name=request.data.get("name"), task=task)
    return Response({"message": "Subtask created", "subtaskID": str(subtask.subtaskID)}, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def delete_subtask(request):
    try:
        subtask = SubTask.objects.get(subtaskID=request.data.get("subtask_id"))
    except SubTask.DoesNotExist:
        return Response({"error": "Subtask not found"}, status=status.HTTP_404_NOT_FOUND)

    subtask.delete()
    return Response({"message": "Subtask deleted"}, status=status.HTTP_200_OK)


@api_view(["POST"])
def update_subtask_status(request):
    new_status = request.data.get("status")
    if new_status not in ["COMPLETE", "INCOMPLETE"]:
        return Response({"error": "status must be COMPLETE or INCOMPLETE"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        subtask = SubTask.objects.get(subtaskID=request.data.get("subtask_id"))
    except SubTask.DoesNotExist:
        return Response({"error": "Subtask not found"}, status=status.HTTP_404_NOT_FOUND)

    subtask.status = new_status
    subtask.save()
    return Response({"message": "Subtask updated", "status": subtask.status}, status=status.HTTP_200_OK)
