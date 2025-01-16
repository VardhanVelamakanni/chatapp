from django.contrib import admin
from django.urls import path
from chat import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.index, name='index'),  # Default to index for the base path
    path('chat/<int:user_id>/', views.chat_view, name='chat_view'),  # Chat with specific user
    path('chat/', views.index, name='chat'),  # Base chat URL redirects to index
]
