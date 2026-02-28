import requests
import json

def registration_test(endpoint, company_uuid):
    """
    Sends a registration request to the API.
    :param endpoint: The URL of the register view (e.g., 'http://127.0.0.1:8000/api/register/')
    :param company_uuid: A valid UUID string of an existing Company in your DB.
    """
    
    # This dictionary matches the 'fields' list in your RegisterSerializer
    registration_data = {
        "username": "testusername",
        "email": "test@example.com",
        "password": "securepassword123",
        "first_name": "Test",
        "last_name": "User",
        "companyID": company_uuid  # This must be a valid UUID from your DB
    }

    try:
        # We use json= instead of params= to send a application/json POST request
        response = requests.post(endpoint, json=registration_data)
        
        print(f"Status Code: {response.status_code}")
        print("Response Body:")
        print(json.dumps(response.json(), indent=4))
        
        return response
    except Exception as e:
        print(f"An error occurred: {e}")


def login_test(request)

# Example Usage:
# Replace with your actual local URL and a real Company UUID from your database
if __name__ == "__main__":
    API_ENDPOINT = "http://127.0.0.1:8000/api/auth/register/"
    # You can find a valid UUID by running: python manage.py shell
    # >>> from api.models import Company; print(Company.objects.first().compID)
    VALID_COMPANY_UUID = "f47ac10b-58cc-4372-a567-0e02b2c3d479"

    registration_test(API_ENDPOINT, VALID_COMPANY_UUID)
