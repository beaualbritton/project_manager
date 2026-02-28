from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Company, Employee

class RegistrationTests(APITestCase):

    def setUp(self):
        # We need a company in the DB first since the serializer requires a companyID
        self.company = Company.objects.create(name="Test Corp")
        self.register_url = reverse('register') # Ensure your urls.py has name='register'

    def test_register_user_success(self):
        """Test that a user and employee profile are created with valid data."""
        data = {
            "username": "owen_test",
            "password": "securepassword123",
            "email": "odavis@gmail.com",
            "first_name": "Owen",
            "last_name": "Davis",
            "companyID": self.company.compID
        }
        
        response = self.client.post(self.register_url, data, format='json')
        
        # Check response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], "User and Employee profile created successfully.")
        
        # Check Database: Does the User exist?
        self.assertTrue(User.objects.filter(username="owen_test").exists())
        
        # Check Database: Does the Employee exist and link to the User?
        user = User.objects.get(username="owen_test")
        self.assertTrue(Employee.objects.filter(user=user).exists())
        self.assertEqual(user.employee_profile.company, self.company)

    def test_register_missing_fields(self):
        """Test that registration fails if required fields are missing."""
        data = {
            "username": "incomplete_user",
            # missing password and companyID
        }
        response = self.client.post(self.register_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        self.assertIn('companyID', response.data)

    def test_duplicate_username(self):
        """Test that you cannot register with a username that already exists."""
        # Create a user manually first
        User.objects.create_user(username="duplicate", password="password123")
        
        data = {
            "username": "duplicate",
            "password": "newpassword123",
            "email": "new@uvm.edu",
            "companyID": self.company.compID
        }
        response = self.client.post(self.register_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)