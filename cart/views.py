from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from properties.models import Property
from .cart import Cart
from django.contrib.auth.decorators import login_required

def cart(request):
    """
    Display the cart details.
    """
    cart = Cart(request)
    return render(request, 'cart.html', {
        'cart': cart,
    })

def add_to_cart(request, property_id):
    """
    Add a property to the cart.
    """
    property = get_object_or_404(Property, id=property_id)
    cart = Cart(request)
    cart.add(property=property)
    return redirect('properties')

def remove_from_cart(request, property_id):
    """
    Remove a property from the cart.
    """
    property = get_object_or_404(Property, id=property_id)
    cart = Cart(request)
    cart.remove(property=property)
    return redirect('cart')

@login_required
def buy_property(request, property_id):
    """
    Simulate buying a property. Remove it from the cart after purchase.
    """
    property = get_object_or_404(Property, id=property_id)
    cart = Cart(request)

    # Simulate the purchase logic
    if str(property.id) in cart.cart:
        cart.remove(property=property)
        # You can implement actual purchase logic here (e.g., creating an order).
        # For now, we just return a success message.
        return JsonResponse({'status': f'Property {property.name} purchased successfully!'})

    return JsonResponse({'status': 'Property not found in cart.'}, status=404)


def load_cart(request):
    """
    Load the cart from the user's saved data.
    """
    cart = Cart(request)
    cart.load_cart_from_user()
    return redirect('cart')

@login_required
def save_cart(request):
    """
    Save the cart to the user's profile.
    """
    cart = Cart(request)
    cart._save_to_user()
    return JsonResponse({'status': 'Cart saved successfully'})
