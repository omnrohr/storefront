from django.db import models
from django.db.models.fields import UUIDField
from uuid import uuid4


class Promotion(models.Model):
    title = models.CharField(max_length=250, null=True, blank=True)
    new_price = models.DecimalField(max_digits=9, decimal_places=2)


class Collection(models.Model):
    title = models.CharField(max_length=150, null=True, blank=True)
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']


class Product(models.Model):
    title = models.CharField(max_length=150)
    unit_price = models.DecimalField(max_digits=9, decimal_places=3)
    slug = models.SlugField()
    weight = models.DecimalField(
        max_digits=9, decimal_places=3, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.URLField(max_length=250, null=True, blank=True)
    sku = models.CharField(max_length=15, null=True, blank=True)
    last_update = models.DateTimeField(auto_now=True)
    inventory = models.BooleanField(default=True)
    collection = models.ForeignKey(
        Collection, on_delete=models.PROTECT, related_name='products')
    tag = models.CharField(max_length=30, null=True, blank=True)
    vendor = models.CharField(max_length=155, null=True, blank=True)
    promotions = models.ManyToManyField(Promotion, related_name='products')


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    f_name = models.CharField(max_length=50, null=True, blank=True)
    l_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(
        max_length=255, unique=True, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True, unique=True)
    birth_date = models.DateField(null=True)
    create_date = models.DateField(auto_now_add=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]
    placed_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, null=True, blank=True, related_name='orders')


class Address(models.Model):
    city = models.CharField(max_length=50, null=True, blank=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    building = models.CharField(max_length=4, null=True, blank=True)
    floor = models.CharField(max_length=3, null=True, blank=True)
    apartment = models.CharField(max_length=4, null=True, blank=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='addresses')


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.PROTECT, null=True, blank=True, related_name='orderitems')
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='orderitems')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(
        max_digits=9, decimal_places=3, null=True, blank=True)


class Cart(models.Model):
    id = UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = [['cart', 'product']]


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=150)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
