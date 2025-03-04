from django.db import models
# from users.models import User
# from users.models import Seller, Trader
from django.conf import settings  # Избегаем цикличного импорта


class Category(models.Model):
    name = models.CharField(max_length=255)
    # store = models.ForeignKey(Store, on_delete=models.CASCADE)
    # store = models.ForeignKey("products.Store", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    # category = models.ForeignKey('Category', on_delete=models.CASCADE) #products.
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)  # Allow NULL temporarily

    # seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name="products")
    # seller = models.ForeignKey(Seller, on_delete=models.CASCADE, default=1)
    # image = models.ImageField(upload_to='products/', null= True, blank=True)
    seller = models.ForeignKey('users.Seller', on_delete=models.CASCADE, related_name="products", null=True, blank=True)
    trader = models.ForeignKey('users.Trader', on_delete=models.SET_NULL, related_name="products", null=True, blank=True)  # Trader тоже может продавать
    image = models.ImageField(upload_to="product_images/", blank=True, null=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def approve(self):
        """Продавец подтверждает товар"""
        self.approved = True
        self.save()


class Store(models.Model):
    name = models.CharField(max_length=255)
    # description = models.TextField(blank=True, null=True)  # Optional
    seller = models.ForeignKey('users.Seller', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=255)
    seller = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="companies")  # Allow multiple companies per user


class ProductRequest(models.Model):
    trader = models.ForeignKey('users.Trader', on_delete=models.CASCADE, related_name="requests")
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="requests")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="requests")
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.05)
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("approved", "Approved"), ("rejected", "Rejected")],
        default="pending"
    )

    def approve(self):
        """Продавец одобряет товар"""
        self.status = "approved"
        self.product.approved = True
        self.product.save()
        self.save()

