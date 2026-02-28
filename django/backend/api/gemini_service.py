import os
from django.conf import settings
from google import genai

# This allows the script to work even if Django isn't fully loaded
def get_client():
    api_key = getattr(settings, "GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))
    return genai.Client(api_key=api_key)

def get_gemini_response(prompt):
    client = get_client()
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text

# --- TESTING BLOCK ---
if __name__ == "__main__":
    # This part allows you to run 'python gemini_service.py' directly
    import sys
    import pathlib
    
    # Add project root to path so settings can be found
    sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    
    import django
    django.setup()

    print(get_gemini_response("Say 'The backend is connected'"))
# Encapsulates all AI logic
import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

def get_gemini_response(prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text
