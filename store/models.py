from django.db import models


class Promotion(models.Model):
    title = models.CharField(max_length=250, null=True, blank=True)
    new_price = models.DecimalField(max_digits=9, decimal_places=2)


class Collection(models.Model):
    title = models.CharField(max_length=150, null=True, blank=True)
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')


class Product(models.Model):
    title = models.CharField(max_length=150, null=True, blank=True)
    unit_price = models.DecimalField(max_digits=9, decimal_places=3, default=1)
    weight = models.DecimalField(
        max_digits=9, decimal_places=3, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.URLField(max_length=250, null=True, blank=True)
    sku = models.CharField(max_length=15, null=True, blank=True)
    last_update = models.DateTimeField(auto_now=True)
    inventory = models.BooleanField(default=True)
    collection = models.ForeignKey(
        Collection, on_delete=models.PROTECT, null=True, blank=True)
    tag = models.CharField(max_length=30, null=True, blank=True)
    vendor = models.CharField(max_length=155, null=True, blank=True)
    promotions = models.ManyToManyField(Promotion, related_name='products')


class Customer(models.Model):
    f_name = models.CharField(max_length=50, null=True, blank=True)
    l_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(
        max_length=255, unique=True, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True, unique=True)
    create_date = models.DateField(auto_now_add=True)


class Order(models.Model):
    ORDER_STATUS = [
        ('VP', 'Pending'),
        ('VS', 'Sending'),
        ('VR', 'Vendor Received'),
        ('VR', 'preparing for dispatch'),
        ('DW', 'On my way'),
        ('DL', 'Delivered'),
        ('VF', 'Failed')
    ]
    placed_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=ORDER_STATUS, default='VP')
    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, null=True, blank=True)


class Address(models.Model):
    city = models.CharField(max_length=50, null=True, blank=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    building = models.CharField(max_length=4, null=True, blank=True)
    floor = models.CharField(max_length=3, null=True, blank=True)
    apartment = models.CharField(max_length=4, null=True, blank=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.PROTECT, null=True, blank=True)
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, null=True, blank=True)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(
        max_digits=9, decimal_places=3, null=True, blank=True)


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
