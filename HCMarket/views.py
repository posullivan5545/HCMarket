# views.py
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product
from django.contrib.auth.decorators import login_required
from .forms import UpdateUserForm, UpdatePasswordForm, ProductForm
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required


def home(request):
    products = Product.objects.filter(is_sold=False) #Only return unsold items to display
    return render(request, 'index.html', {'products': products})
@login_required
def acchome(request):
    if request.user.is_authenticated:
        products = Product.objects.filter(is_sold=False) #Only return unsold items to display
        content = {'username': request.user.username, 'products': products}
        return render(request, 'signedinhome.html', content)
    else:
        return HttpResponseRedirect('/signin')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        if not email.endswith('@g.holycross.edu'):
            messages.error(request, 'Email must be a Holy Cross email address.')
            return render(request, 'signup.html')
        if User.objects.filter(username=username).exists(): #check if user already exists
            messages.error(request, 'Username already taken. Please choose a different username.')
            return render(request, 'signup.html')
        
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        
        login(request, user)
        return HttpResponseRedirect('/acchome')
    return render(request, 'signup.html')

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        password_form = UpdatePasswordForm(request.user, request.POST)
        
        if user_form.is_valid() and password_form.is_valid():
            user_form.save()
            password_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile.html')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UpdateUserForm(instance=request.user)
        password_form = UpdatePasswordForm(request.user)
    
    products = Product.objects.filter(seller=request.user)
    
    context = {
        'user_form': user_form,
        'password_form': password_form,
        'products': products
    }
    
    return render(request, 'profile.html', context)

@login_required
def edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'form': form, 'product_name': product.name})
@login_required
def delete_product(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        product.delete()
        return HttpResponseRedirect('/profile')
    return render(request, 'profile.html', {'product': product})
# Change render / redirect, delete works just bugs out profile page. 
def view_product(request, id):
    try:
        product = Product.objects.get(id=id)
        data = {
            'name': product.name,
            'description': product.description,
            'seller': product.seller.email,
            'in_negotiation': product.in_negotiation
        }
        return JsonResponse(data)
    except:
        return JsonResponse({'error': 'Product not found'}, status=404)
    
@login_required
def list_item(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        #Come back to if time, not originally working in removing these two from form to list item.
        #form.fields.pop('is_sold')
        #form.fields.pop('in_negotiation')
        if form.is_valid():
            product = form.save(commit=False) # Delayed saving to database
            product.seller = request.user
            product.save()
            return redirect('profile')
    else:
        form = ProductForm()
    return render(request, 'list_item.html', {'form': form})

def search(request):
    query = request.GET.get('query', '').strip()  # Get the search query from the GET parameters
    if query:
        # Perform a case-insensitive search on the 'name' and 'description' fields of the Product model
        products = Product.objects.filter(name__icontains=query) | Product.objects.filter(description__icontains=query)
    else:
        products = Product.objects.all()  # If no query is provided, return all products

    context = {
        'products': products,
        'query': query,  # Include the query for display purposes (optional)
    }
    return render(request, 'search_results.html', context)


        


