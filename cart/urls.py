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
from cart import views

urlpatterns = [
    path('', views.cart, name='cart'),  # Display cart
    path('add_to_cart/<int:property_id>/', views.add_to_cart, name='add_to_cart'),  # Add property to cart
    path('remove_from_cart/<int:property_id>/', views.remove_from_cart, name='remove_from_cart'),  # Remove property from cart
    path('buy_property/<int:property_id>/', views.buy_property, name='buy_property'),  # Buy property from cart
    path('load/', views.load_cart, name='load_cart'),
    path('save/', views.save_cart, name='save_cart'),
]
