# views.py
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product

def home(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})

def acchome(request):
    if request.user.is_authenticated:
        products = Product.objects.all()
        content = {'username': request.user.username, 'products': products}
        return render(request, 'signedinhome.html', content)
    else:
        return HttpResponseRedirect('/signin')

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

def signin(request): 
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        print(f"User authenticated: {user}")
        if user is not None:
            login(request, user)
            username = user.username
            return render(request, 'acchome.html', {'username': username})
        else:
            messages.error(request, 'Invalid credentials.')
            return render(request, 'signin.html')
    return render(request, 'signin.html')

def signout(request):
    logout(request)
    return HttpResponseRedirect('/')

def profile(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/home')  
    
    user = request.user
    products = Product.objects.filter(user=user)
        
    context = {
        'username': user.username,
        'email': user.email,
        'products': products
    }
        
    return render(request, 'profile.html', context)


#Next Steps:
# Product Info Popup for signed in users
# Sell Item popup to create and list an item