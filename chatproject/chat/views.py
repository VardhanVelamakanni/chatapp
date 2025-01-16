from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Message
import logging
from django import forms

logger = logging.getLogger(__name__)

def login_view(request):
    """
    Handles user login.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            logger.info(f"User {user.username} logged in successfully.")
            return redirect('index')  # Redirect to the index page
        else:
            logger.warning("Invalid login attempt.")
            return render(request, 'chat/login.html', {'form': form, 'error': 'Invalid username or password'})
    else:
        form = AuthenticationForm()
    return render(request, 'chat/login.html', {'form': form})
class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username'}),
        max_length=10 # You can increase or remove max_length if required
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
def signup(request):
    """
    Handles user signup.
    """
    if request.method == 'POST':
        logger.info("Signup POST request received.")
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in after signup
            logger.info(f"User {user.username} signed up successfully.")
            return redirect('index')  # Redirect to the index page
        else:
            logger.error("Signup form is invalid.")
            return render(request, 'chat/signup.html', {'form': form, 'error': 'Form is invalid. Please correct the errors below.'})
    else:
        logger.info("Signup GET request received.")
        form = UserCreationForm()
    return render(request, 'chat/signup.html', {'form': form})

def logout_view(request):
    """
    Handles user logout.
    """
    logout(request)
    logger.info(f"User logged out successfully.")
    return redirect('login')  # Redirect to the login page

@login_required
def index(request):
    """
    Displays all users except the logged-in one.
    """
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/index.html', {'users': users, 'page_type': 'users'})

@login_required
def chat_view(request, user_id):
    """
    Displays the chat between the logged-in user and the selected user.
    """
    recipient = get_object_or_404(User, id=user_id)
    users = User.objects.exclude(id=request.user.id)

    # Fetch chat messages
    messages = Message.objects.filter(
        Q(sender=request.user, recipient=recipient) |
        Q(sender=recipient, recipient=request.user)
    ).order_by('timestamp')

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                sender=request.user,
                recipient=recipient,
                content=content
            )
        return redirect('chat_view', user_id=user_id)  # Redirect back to the chat view

    return render(request, 'chat/chat.html', {
        'recipient': recipient,
        'users': users,
        'messages': messages,
        'page_type': 'chat',
    })

@login_required
def send_message(request, user_id):
    """
    Handles sending messages to the selected user.
    """
    recipient = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            create_message(request.user, recipient, content)
        return redirect('chat_view', user_id=user_id)

def create_message(sender, recipient, content):
    """
    Creates a message object and saves it to the database.
    """
    Message.objects.create(sender=sender, recipient=recipient, content=content)

@login_required
def chat_home(request):
    """
    Handles requests to /chat/ by redirecting to the main chat index.
    """
    return redirect('index')