from decimal import Decimal
from rest_framework import serializers
from store.models import Product, Collection, Review


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    """
    This class return a Json Response with information spicified bellow.

    With this method is less coding adn the same result
    If you add a field in fields dictoinary and this field was not the original class 
    rest frame work will search for this field in the same class like the price with tax method blow 
    """
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price',
                  'price_with_tax', 'slug', 'inventory', 'collection', 'description']
        #   ['collection_ref', 'nested_collection', 'collectin_link']

    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.16)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)
