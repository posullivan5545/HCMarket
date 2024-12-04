# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Product
from django.contrib.auth.forms import PasswordChangeForm

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

class UpdatePasswordForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['password']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image_url','is_sold', 'in_negotiation']