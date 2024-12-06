from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# Custom Manager for NewUser
class NewUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email, password, and additional fields.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)  # Normalize email
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, **extra_fields)  # Create user instance
        user.set_password(password)  # Set hashed password
        user.save(using=self._db)  # Save user to the database
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email, password, and additional fields.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

# Custom User model
class NewUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = NewUserManager()  # Use the custom manager

    USERNAME_FIELD = 'email'  # Email is the unique identifier
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Required fields when creating superuser

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    def has_perm(self, perm, obj=None):
        """
        Return True if the user has the given permission.
        """
        return self.is_superuser or super().has_perm(perm, obj)

    def has_module_perms(self, app_label):
        """
        Return True if the user has permission to access the given app.
        """
        return self.is_superuser or super().has_module_perms(app_label)

# Profile model related to the NewUser model
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    date_modified = models.DateTimeField(auto_now=True)
    phone = models.CharField(max_length=20, blank=True)  # Store user's phone number
    address1 = models.CharField(max_length=50, blank=True)  # Primary address field
    address2 = models.CharField(max_length=50, blank=True)  # Secondary address field (optional)
    city = models.CharField(max_length=50, blank=True)  # City
    zipcode = models.CharField(max_length=50, blank=True)  # Zip code
    country = models.CharField(max_length=50, blank=True)  # Country
    old_cart = models.JSONField(blank=True, null=True)  # Store old cart data in JSON format

    def __str__(self):
        return self.user.email if self.user else "Unlinked Profile"

# Signals to create or delete the profile when the user is created or deleted
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    """
    Create a profile for the user when a new user is created.
    """
    if created:
        Profile.objects.create(user=instance)

@receiver(post_delete, sender=settings.AUTH_USER_MODEL)
def delete_profile(sender, instance, **kwargs):
    """
    Delete the profile when the user is deleted.
    """
    if hasattr(instance, 'profile'):
        instance.profile.delete()
