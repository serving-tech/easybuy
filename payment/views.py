from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings

# Create your views here.
from cart.cart import Cart

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from visitor.models import Profile
from .models import Billing
from .forms import BillingForm
from properties.models import Property
from cart.cart import Cart

from django_daraja.mpesa.core import MpesaClient
from rest_framework import status
from rest_framework.decorators import api_view

from .serializers import CustomerSerializer


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Billing
from .forms import BillingForm
from properties.models import Property
from cart.cart import Cart
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django_daraja.mpesa.core import MpesaClient
from properties.models import Property
from .forms import MpesaForm


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Payment
from .forms import PaymentForm
from properties.models import Property
from cart.cart import Cart

@login_required
def billing(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    cart = Cart(request)

    if request.method == 'POST':
        form = BillingForm(request.POST)
        if form.is_valid():
            billing = form.save(commit=False)
            billing.user = request.user
            billing.property = property
            billing.save()

            # Remove item from cart after billing
            cart.remove(property)
            messages.success(request, 'Billing information submitted successfully.')
            return redirect('mpesa', property_id=property_id)  # Correctly redirect to the mpesa view
    else:
        form = BillingForm()

    return render(request, 'billing.html', {'form': form, 'property': property})


def payment_success(request):
    return render(request, 'payment_success.html')

from django.shortcuts import render

def custom_404(request, exception=None):
    return render(request, '404.html', status=404)


@login_required
def payment(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    cart = Cart(request)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.property = property
            payment.save()

            # Remove item from cart after payment
            cart.remove(property)
            messages.success(request, 'Payment completed successfully.')
            return redirect('payment_success')
    else:
        form = PaymentForm()

    return render(request, 'payment.html', {'form': form, 'property': property})


@api_view(['GET', 'POST'])
def customerapi(request):
    if request.method == 'GET':
        profile = Profile.objects.get(user=request.user)
        serializer = CustomerSerializer(profile, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required
def mpesaapi(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    if request.method == 'POST':
        form = MpesaForm(request.POST, user=request.user)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            account_reference = form.cleaned_data['account_reference']
            transaction_desc = form.cleaned_data['transaction_desc']
            amount = int(property.price)  # Ensure the amount is an integer
            callback_url = 'https://darajambili.herokuapp.com/express-payment'

            client = MpesaClient()
            response = client.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)

            # Access the response correctly
            if response.response_code == '0':  # Adjust based on actual attribute/method name
                return redirect('payment_success')
            else:
                return HttpResponse('Payment failed: ' + response.response_description,
                                    status=400)  # Adjust based on actual attribute/method name
    else:
        form = MpesaForm(user=request.user)

    return render(request, 'mpesa.html', {'form': form, 'property': property})

