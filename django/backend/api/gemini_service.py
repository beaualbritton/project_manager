# Encapsulates all AI logic
import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

def get_gemini_response(prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text