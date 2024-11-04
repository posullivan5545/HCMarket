# views.py
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages

def home(request):
    return render(request, 'index.html')

def acchome(request):
    return render(request, 'signedinhome.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        if User.objects.filter(username=username).exists(): #check if user already exists
            messages.error(request, 'Username already taken. Please choose a different username.')
            return render(request, 'signup.html')
        
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        
        login(request, user)
        return HttpResponseRedirect('/acchome') #goes to home page with user privilages
    return render(request, 'signup.html')

def signin(request): #sign in function is broken, tried to debug got nowhere(brandon)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/acchome')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'signin.html')

def signout(request):
    logout(request)
    return HttpResponseRedirect('/')