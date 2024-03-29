"""
URL configuration for CharityDonation project.

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
from django.urls import path, include

from CharityAPP import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.LandingPage.as_view(), name='LandingPage'),
    path('add_donation/', views.AddDonation.as_view(), name='AddDonation'),
    path('form-confirmation/', views.Confirmation.as_view(), name='Confirmation'),
    path('profile/', views.UserProfile.as_view(), name='profile'),
    path('take_donation/<int:donation_id>/', views.TakeDonation.as_view(), name='take_donation'),
    path('settings/', views.settings, name='settings'),
    path('change-password/', views.change_password, name='change_password'),


    path('accounts/', include('accounts.urls')),
]
