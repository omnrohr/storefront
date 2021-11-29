from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=150, null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=1)
    weight = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.URLField(max_length=250, null=True, blank=True)
    sku = models.CharField(max_length=15, null=True, blank=True)
    last_update = models.DateTimeField(auto_now=True)
    inventory = models.BooleanField(default=True)
    tag = models.CharField(max_length=30, null=True, blank=True)
    vendor = models.CharField(max_length=155, null=True, blank=True)


class Customer(models.Model):
    f_name = models.CharField(max_length=50, null=True, blank=True)
    l_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(
        max_length=255, unique=True, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True, unique=True)
    create_date = models.DateField(auto_now_add=True)
