from decimal import Decimal
from rest_framework import serializers

from store.models import Product, Collection


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=150)
    # to rename the field from unit_price to price I added source method
    price = serializers.DecimalField(
        max_digits=9, decimal_places=3, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')
    collection = serializers.PrimaryKeyRelatedField(
        queryset=Collection.objects.all()
    )
    collection_ref = serializers.StringRelatedField(source='collection')

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.16)
