import json
from decimal import Decimal
from django.conf import settings
from django.contrib.auth import get_user_model
from properties.models import Property

# Get the custom user model
User = get_user_model()

class Cart:
    def __init__(self, request):
        self.session = request.session
        self.request = request
        self.cart = self.session.get('cart', {})
        if not self.cart:
            self.session['cart'] = self.cart

    def add(self, property):
        property_id = str(property.id)
        if property_id not in self.cart:
            self.cart[property_id] = {'price': str(property.price)}
        self._save_to_session()

    def remove(self, property):
        property_id = str(property.id)
        if property_id in self.cart:
            del self.cart[property_id]
            self._save_to_session()

    def clear(self):
        self.cart = {}
        self._save_to_session()

    def __iter__(self):
        property_ids = self.cart.keys()
        properties = Property.objects.filter(id__in=property_ids)
        cart_copy = self.cart.copy()
        for property in properties:
            property_id = str(property.id)
            cart_copy[property_id]['property'] = property
        for item in cart_copy.values():
            item['price'] = Decimal(item['price'])
            yield item

    def __len__(self):
        return len(self.cart)

    def get_total_price(self):
        return sum(Decimal(item['price']) for item in self.cart.values())

    def _save_to_session(self):
        self.session['cart'] = self.cart
        self.session.modified = True
        if self.request.user.is_authenticated:
            self._save_to_user()

    def _save_to_user(self):
        """Save the cart data to the user's profile in the database."""
        try:
            current_user = User.objects.get(id=self.request.user.id)
            cart_data = json.dumps(self.cart)
            current_user.old_cart = cart_data
            current_user.save()
        except User.DoesNotExist:
            pass

    def load_cart_from_user(self):
        """Load the cart from the user's profile if the user is authenticated."""
        if self.request.user.is_authenticated:
            try:
                current_user = User.objects.get(id=self.request.user.id)
                saved_cart = current_user.old_cart
                if saved_cart:
                    try:
                        converted_cart = json.loads(saved_cart)
                        for property_id, item in converted_cart.items():
                            property = Property.objects.get(id=int(property_id))
                            self.add(property=property)
                    except json.JSONDecodeError:
                        pass
            except User.DoesNotExist:
                pass
