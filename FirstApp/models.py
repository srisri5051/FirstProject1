from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    
    user_details = models.CharField(max_length=100, blank=True, null=True)
    dealer_details = models.CharField(max_length=100, blank=True, null=True)

    class Role(models.TextChoices):
        USERS = 'user'
        DEALER = 'dealer'
        ADMIN = 'admin'
        
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.USERS)

    def __str__(self):
        return self.username
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    dealer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True, related_name='products')
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', blank=True, null=True, verbose_name=("Category"))
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    comments = models.TextField(blank=True, null=True)
    
    
    def __str__(self):
        return self.name



class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)




