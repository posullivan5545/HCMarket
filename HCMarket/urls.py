"""
URL configuration for HCMarket project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views 
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path(
        'signin/',
        auth_views.LoginView.as_view(
            template_name='signin.html',
            redirect_authenticated_user=True,
            next_page='/acchome'
        ),
        name='signin'
    ),
    path('logout/', auth_views.LogoutView.as_view(next_page='/signin'), name='logout'),
    path('acchome/', views.acchome, name='acchome'),
    path('profile/', views.profile, name='profile'),
    path('edit_product/<int:id>/', views.edit_product, name='edit_product'),
    path('profile/delete/<int:id>/', views.delete_product, name='delete_product'),
    path('product/<int:id>/', views.view_product, name='product'),
]
