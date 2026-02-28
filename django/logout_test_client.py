import requests
import json

def test_full_auth_cycle(base_url, username, password):
    """
    Tests Login -> Check Status -> Logout -> Check Status again.
    """
    session = requests.Session()
    
    # 1. LOGIN
    login_url = f"{base_url}login/"
    login_data = {"username": username, "password": password}
    
    print(f"--- 1. Attempting Login ---")
    login_response = session.post(login_url, json=login_data)
    
    if login_response.status_code != 200:
        print(f"Login failed with status {login_response.status_code}")
        return

    # Extract CSRF token from the response JSON (provided by your login view)
    login_json = login_response.json()
    csrf_token = session.get(f'{base_url}/csrf/')
    #csrf_token = csrf_token.data
    print(csrf_token)
    print("Login Successful. Token retrieved.")

    # 2. VERIFY AUTH (Check endpoint)
    check_url = f"{base_url}check/"
    check_resp = session.get(check_url)
    print(f"--- 2. Auth Check (Pre-Logout): {check_resp.status_code} ---")

    # 3. LOGOUT
    # IMPORTANT: We must send the X-CSRFToken header for POST requests
    logout_url = f"{base_url}logout/"
    headers = {
        "X-CSRFToken": csrf_token,
        "Referer": base_url # Some Django configs require Referer for CSRF
    }
    
    print(f"--- 3. Attempting Logout ---")
    logout_response = session.post(logout_url, headers=headers)
    
    if logout_response.status_code == 200:
        print("Logout Successful:", logout_response.json().get('message'))
    else:
        print(f"Logout Failed: {logout_response.status_code}")
        print(logout_response.text[:200])

    # 4. VERIFY LOGOUT (Check endpoint again)
    final_check = session.get(check_url)
    # If using Session Auth, this usually returns 403 or shows AnonymousUser
    print(f"--- 4. Auth Check (Post-Logout): {final_check.status_code} ---")

if __name__ == "__main__":
    # Ensure this matches your ACTUAL URL exactly (including the /auth/ part if that's in your urls.py)
    # Based on your prompt: /api/auth/logout/
    BASE_API_URL = "http://127.0.0.1:8000/api/auth/"
    
    # Use your test credentials
    USER = "testusername"
    PASS = "securepassword123"
    
    test_full_auth_cycle(BASE_API_URL, USER, PASS)
