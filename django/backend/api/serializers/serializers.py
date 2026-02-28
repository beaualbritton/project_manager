from django.contrib.auth.models import User
from rest_framework import serializers
from ..models import Employee, Company

class RegisterSerializer(serializers.ModelSerializer):
    # These fields are for the User model
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)

    # This field is for the Employee model
    companyID = serializers.UUIDField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'companyID']

    def create(self, validated_data):
        # 1. Extract the data meant for the Employee/Company
        company_id = validated_data.pop('compID')

        # 2. Create the User
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )

        # 3. Find the Company and create the Employee
        try:
            company = Company.objects.get(compID=company_id)
        except Company.DoesNotExist:
            # If for some reason the company is missing, we still need to create the profile
            company = None

        Employee.objects.create(
            user=user,
            company=company
        )

        return user


class EmployeeListSerializer(serializers.ModelSerializer):
    # Pull fields from the related User model
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)

    # Pull the company name instead of just the UUID
    company_name = serializers.CharField(source='company.name', read_only=True)

    class Meta:
        model = Employee
        fields = [
            'employeeID', 
            'username', 
            'email', 
            'first_name', 
            'last_name', 
            'position', 
            'company', 
            'company_name'
        ]
