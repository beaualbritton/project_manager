from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Employee

class RegisterSerializer(serializers.ModelSerializer):
    # We use 'name' as the input field but map it to 'username' in the database
    name = serializers.CharField(source='username')
    password = serializers.CharField(write_only=True, min_length=8)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['name', 'email', 'password']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        # 1. Create the base User
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        # 2. Create the Employee profile linked to that User
        # The employeeID (UUID) is generated automatically by your model
        Employee.objects.create(user=user)
        
        return user
