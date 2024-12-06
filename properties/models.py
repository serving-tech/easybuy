from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.core.validators import FileExtensionValidator
from decimal import Decimal, InvalidOperation


class Property(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/',
                              validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])
    image1 = models.ImageField(upload_to='images/',
                              validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])], null=True, blank=True)
    image2 = models.ImageField(upload_to='images/',
                              validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])], null=True, blank=True)
    image3 = models.ImageField(upload_to='images/',
                              validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])], null=True, blank=True)
    video_url = models.URLField(max_length=600, null=True, blank=True)

    status = models.CharField(max_length=50, default='Pending')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    area = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    beds = models.IntegerField(default=0)
    baths = models.IntegerField(default=0)
    garage = models.IntegerField(default=0)
    key = models.CharField(max_length=10, unique=True)
    location = models.CharField(max_length=100)
    map_url = models.URLField(max_length=600, null=True, blank=True)
    propertytyp = models.CharField(max_length=50, default='House')
    description = models.TextField(default='A great House at the brink of existence.')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        try:
            # Ensure empty strings are treated as None for Decimal fields
            if self.price == '':
                self.price = None
            if self.area == '':
                self.area = 0.0

            # Convert price and area to valid Decimal values
            self.price = Decimal(self.price) if self.price is not None else None
            self.area = Decimal(self.area) if self.area is not None else 0.0
        except (InvalidOperation, TypeError):
            raise ValueError("Price and area must be decimal numbers")

        # Call the parent save method
        super(Property, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100, choices=[('general', 'General Inquiry'), ('feedback', 'Feedback')])
    message = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"


class Partners(models.Model):
    image = models.ImageField(upload_to='images/', validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])  # Moved to a subfolder
    name = models.CharField(max_length=100)
    details = models.CharField(max_length=100, default='We are committed to bring to you the best properties. ')
    facebook = models.URLField(max_length=200, blank=True, null=True)
    instagram = models.URLField(max_length=200, blank=True, null=True)
    linkedin = models.URLField(max_length=200, blank=True, null=True)
    twitter = models.URLField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Agent"
        verbose_name_plural = "Agents"


class Testimonials(models.Model):
    image = models.ImageField(upload_to='testimonials/images/', validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])  # Moved to a subfolder
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100, default='CEO')
    testimony = models.TextField()
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"


