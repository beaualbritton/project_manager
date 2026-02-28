"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api.views import check, csrf_token, login, register, logout, get_employee_list
from api.views.gemini import GeminiChatView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/chat/', GeminiChatView.as_view(), name='gemini-chat'),
    path('api/auth/check/', check),
    path('api/auth/csrf/', csrf_token),
    path('api/auth/login/', login, name='login'),
    path('api/auth/register/', register, name='register'),
    path('api/auth/logout/', logout),

    path('api/employees/get_all', get_employee_list),
]
