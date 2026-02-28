import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Company(models.Model):
    compID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Team(models.Model):
    teamID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    leader = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True, related_name='led_teams')

    def __str__(self):
        return f"{self.name} ({self.company.name})"

class Employee(models.Model):
    employeeID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # This links the Employee to the built-in Django User
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    # Your custom Hackathon fields
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    # If an employee can be in multiple teams, use ManyToMany
    teams = models.ManyToManyField('Team', blank=True) 

    POSITION_CHOICES = [
        ('LEAD', 'Team Lead'),
        ('MEMBER', 'Member'),
    ]
    position = models.CharField(max_length=10, choices=POSITION_CHOICES, default='MEMBER')
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employees', null=True)
    
    # This creates the "teamID's list" relationship
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