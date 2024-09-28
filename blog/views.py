from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'authentication/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid username or password'
    else:
        error_message = ''
    return render(request, 'authentication/login.html', {'error_message': error_message})

def user_logout(request):
    logout(request)
    return redirect('login')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    # Access the authenticated user directly
    user = request.user.username  # Get the username of the authenticated user
    return render(request, 'authentication/home.html', {'user': user})