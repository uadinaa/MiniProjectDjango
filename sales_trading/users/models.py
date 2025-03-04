from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User

from products.models import Product


# from products.models import Store
# from django.contrib.auth import get_user_model

# User = get_user_model()


class User(AbstractUser):

    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=100000.00)

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('seller', 'Seller'),
        ('trader', 'Trader'),
        ('customer', 'Customer'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='customer',  # Set a default role
        db_index=True  # Optimize queries by role
    )

    groups = models.ManyToManyField(
        "auth.Group",  # This should correctly refer to the auth app's Group model
        related_name="custom_user_set",
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",  # Ensure this is referencing the correct model
        related_name="custom_user_permissions_set",
        blank=True,
    )


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    avatar_url = models.URLField(null=True, blank=True)  # Store URL instead of file
#

@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:  # If a new user is created
        Customer.objects.create(user=instance)


class Seller(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sellers")  # Allow multiple companies per user
    company_name = models.CharField(max_length=255)
    company_logo = models.URLField(null=True, blank=True)  # Store URL instead of file

    def __str__(self):
        return self.user.username  # Now DRF will display the username instead of "Seller object (1)"


class Trader(models.Model):  # Было SellsRepresentative
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="trader")
    stores = models.ManyToManyField("products.Store", related_name="traders")  # Может подключаться к магазинам
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.05)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)


class Purchase(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=1)
    purchase_date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

