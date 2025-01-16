from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Message
from django.db.models import Q
from django.contrib.auth.models import User


def login_view(request):
    """
    Handles user login.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')  # Redirect to the index page
    else:
        form = AuthenticationForm()

    return render(request, 'chat/login.html', {'form': form})

def signup(request):
    """
    Handles user registration.
    """
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
    """
    Displays all users except the logged-in one.
    """
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/index.html', {'users': users})

@login_required
def chat_view(request, user_id):
    """
    Displays the chat between the logged-in user and the selected user.
    """
    recipient = get_object_or_404(User, id=user_id)  # Get the recipient by user_id
    messages = Message.objects.filter(
        Q(sender=request.user, recipient=recipient) |
        Q(sender=recipient, recipient=request.user)
    ).order_by('timestamp')  # Fetch messages between logged-in user and recipient

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            create_message(request.user, recipient, content)  # Save the message in the database
        return redirect('chat_view', user_id=user_id)

    return render(request, 'chat/chat.html', {
        'recipient': recipient,
        'messages': messages,
        'user': request.user,
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
            # Save the message in the database
            create_message(request.user, recipient, content)
        # Redirect back to the chat view
        return redirect('chat_view', user_id=user_id)
