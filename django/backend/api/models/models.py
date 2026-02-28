from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Company(models.Model):
    compID = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=100)

class Employee(models.Model):
    # This links the Employee to the built-in Django User
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    
    # Your custom Hackathon fields
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    # If an employee can be in multiple teams, use ManyToMany
    teams = models.ManyToManyField('Team', blank=True) 

    def __str__(self):
        return f"{self.user.username} - {self.company.name if self.company else 'No Company'}"

class Team(models.Model):
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
