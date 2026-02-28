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
    # Mapping model fields to specific JSON keys with capitalization
    EmployeeID = serializers.UUIDField(source='employeeID')
    
    # Concatenating first and last name
    Name = serializers.SerializerMethodField()
    
    # Using get_position_display to get "Team Lead" instead of "LEAD"
    Position = serializers.CharField(source='get_position_display')
    
    # Pulling just the UUIDs of the teams into a list
    teamIDs = serializers.PrimaryKeyRelatedField(
        many=True, 
        read_only=True, 
        source='teams'
    )
    
    # Pulling the specific company UUID
    companyID = serializers.UUIDField(source='company.compID', allow_null=True)
    
    # Pulling email from the related User model
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = Employee
        fields = ['EmployeeID', 'Name', 'Position', 'teamIDs', 'companyID', 'email']

    def get_Name(self, obj):
        # Combines first and last name, or falls back to username if names aren't set
        full_name = f"{obj.user.first_name} {obj.user.last_name}".strip()
        return full_name if full_name else obj.user.username
