from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('chat.urls')),  # Include the chat app URLs
    path('', lambda request: redirect('chat/', permanent=True)),  # Redirect root to /chat/
]
