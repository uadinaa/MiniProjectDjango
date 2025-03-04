from django.db import models
# from product.models import User, Customer

from products.models import Product
from users.models import Customer, Seller, Trader, User



# class Order(models.Model):
#     customer = models.ForeignKey(User, on_delete=models.CASCADE)
#     store = models.ForeignKey(Store, on_delete=models.CASCADE)
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('canceled', 'Canceled')])
#     created_at = models.DateTimeField(auto_now_add=True)


class PurchaseRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'waittiing'),
        ('approved', 'approveed'),
        ('declined', 'decLined'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    trader = models.ForeignKey(Trader, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    # buyer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Accept both Trader & Customer


class Receipt(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    trader = models.ForeignKey(Trader, on_delete=models.CASCADE, null=True, blank=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Receipt #{self.id} - {self.product.name}"

