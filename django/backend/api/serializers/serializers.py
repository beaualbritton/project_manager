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
        company_id = validated_data.pop('companyID')
        
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
