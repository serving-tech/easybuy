from django.conf import settings

from properties.models import Property
from django.db import models
from django.core.validators import RegexValidator

class Billing(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    phone = models.CharField(
        max_length=20,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')]  # Example for validating phone number
    )
    email = models.EmailField()

    def __str__(self):
        return f"{self.user.email}'s billing details for {self.property.title}"


from django.db import models

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True)
    card_number = models.CharField(max_length=16, blank=True)  # Only store the last 4 digits, or use tokenization
    card_holder = models.CharField(max_length=100)
    expiration_date = models.CharField(max_length=5)  # Consider using a DateField instead
    cvv = models.CharField(max_length=3)  # Ensure this is not stored if you are PCI-DSS compliant
    billing_address = models.TextField()

    def __str__(self):
        return f"Payment by {self.user.username} for {self.property.title}"

