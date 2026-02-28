import uuid
from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    compID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    def __str__(self): return self.name

class Team(models.Model):
    teamID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='teams')
    leader = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True, related_name='led_teams')
    def __str__(self): return f"{self.name} ({self.company.name})"

class Employee(models.Model):
    employeeID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    
    POSITION_CHOICES = [
        ('LEAD', 'Team Lead'),
        ('MEMBER', 'Member'),
    ]
    position = models.CharField(max_length=10, choices=POSITION_CHOICES, default='MEMBER')
    
    # Fixed: Removed duplicates and kept the detailed versions
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employees', null=True)
    teams = models.ManyToManyField(Team, blank=True, related_name='members')

    def __str__(self):
        return f"{self.user.username} - {self.company.name if self.company else 'No Company'}"

class Task(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETE', 'Complete'),
    ]

    taskID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    
    # Links task to a Team
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.name

class SubTask(models.Model):
    STATUS_CHOICES = [
        ('COMPLETE', 'Complete'),
        ('INCOMPLETE', 'Incomplete')
    ]

    subtaskID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='INCOMPLETE')
    
    # Links subtask to a task
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')

    def __str__(self):
        return self.name
