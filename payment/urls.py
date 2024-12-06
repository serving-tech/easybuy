from django.contrib import admin
from django.urls import path, include
from payment import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('billing/<int:property_id>/', views.billing, name='billing'),
    path('payment/<int:property_id>/', views.payment, name='payment'),
    path('mpesa/<int:property_id>/', views.mpesaapi, name='mpesa'),
    path('customerapi/', views.customerapi, name='customerapi'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('visitor/',include('visitor.urls'))
]

