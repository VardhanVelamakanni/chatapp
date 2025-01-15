from django.contrib.auth.forms import AuthenticationForm  # Add this import
from django.contrib.auth import login, authenticate
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required  # Import the decorator
from django.db.models import Q  # Import Q for filtering with OR conditions
from .models import Message
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')  # Redirect to the index page
    else:
        form = AuthenticationForm()

    return render(request, 'chat/login.html', {'form': form})

    return render(request, 'chat/login.html', {'form': form})
# Index view (Displays all users except the logged-in one)
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after successful signup
            return redirect('index')  # Redirect to index page after signup
    else:
        form = UserCreationForm()

    return render(request, 'chat/signup.html', {'form': form})
@login_required
def index(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/index.html', {'users': users})

# Signup view (Handles user registration)

 # Ensure only logged-in users can access this view
def chat_view(request, user_id):
    recipient = get_object_or_404(User, id=user_id)
    
    # Get chat messages between logged-in user and the recipient
    messages = Message.objects.filter(
        Q(sender=request.user, recipient=recipient) | Q(sender=recipient, recipient=request.user)
    ).order_by('timestamp')
    
    if request.method == 'POST':
        content = request.POST.get('content')
        Message.objects.create(sender=request.user, recipient=recipient, content=content)
    
    return render(request, 'chat/chat.html', {'recipient': recipient, 'messages': messages})

