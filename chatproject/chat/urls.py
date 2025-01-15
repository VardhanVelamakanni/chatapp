# chat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),  # Login page
    path('chat/<int:user_id>/', views.chat_view, name='chat'),  # Chat page with a specific user
    path('signup/', views.signup, name='signup'),  # Signup page
    path('', views.index, name='index'),  # Index page (list of users)
]
