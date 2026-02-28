import requests
import json

def login_test(endpoint, username, password):
    """
    Simulates an external client logging into the Django API.
    """
    # Create a session object to persist cookies (important for Session Auth)
    session = requests.Session()

    login_data = {
        "username": username,
        "password": password
    }

    try:
        print(f"--- Attempting login for user: {username} ---")
        response = session.post(endpoint, json=login_data)
        
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print("Login Successful!")
            print(json.dumps(data, indent=4))
            
            # Extract the CSRF token from the response body (as provided by your view)
            csrf_token = data.get('csrfToken')
            csrf_token = session.get("http://127.0.0.1:8000/api/auth/csrf/")
            print(f"\nCSRF Token received: {csrf_token}")
            
            # --- BONUS: Test the 'check' endpoint using the session ---
            # We use the same 'session' object because it holds our login cookie
            check_url = endpoint.replace('login/', 'check/')
            check_response = session.get(check_url)
            print(f"\nTesting 'check' endpoint status: {check_response.status_code}")

        elif response.status_code == 401:
            print("Login Failed: Invalid credentials.")
            print(response.json())
        else:
            print(f"Error: Received status {response.status_code}")
            print(response.text[:200]) # Print first 200 chars of HTML if it's a 404/500

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # 1. Ensure your server is running: python manage.py runserver
    # 2. Update the URL to match your urls.py exactly (including the trailing slash)
    LOGIN_ENDPOINT = "http://127.0.0.1:8000/api/auth/login/"
    
    # 3. Use the credentials you registered earlier
    TEST_USER = "testusername"
    TEST_PASS = "securepassword123"

    login_test(LOGIN_ENDPOINT, TEST_USER, TEST_PASS)
