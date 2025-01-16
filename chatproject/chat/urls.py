from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('chat/', views.index, name='index'),
    path('chat/<int:user_id>/', views.chat_view, name='chat_view'),
    path('send_message/<int:user_id>/', views.send_message, name='send_message'),
    path('logout/', views.logout_view, name='logout'),
]
