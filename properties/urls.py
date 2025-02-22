"""
URL configuration for hnm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('agents/', views.agents, name='agents'),
    path('contact/', views.contact, name='contact'),
    path('properties/', views.properties, name='properties'),
    path('properties/<int:property_id>/', views.propertysingle, name='propertysingle'),
    path('services/', views.services, name='services'),
    path('servicedetails/', views.servicedetails, name='servicedetails'),
    path('search/', views.search, name='search'),
]
handler404 = 'properties.views.custom_404'