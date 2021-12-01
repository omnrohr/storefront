from decimal import Decimal
from rest_framework import serializers


from store.models import Product, Collection


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=150)
    products_count = serializers.IntegerField(read_only=True)


# class ProductSerializer(serializers.Serializer):
#     """
#     This class return a Json Response with information spicified bellow.

#     If you want to go with serializer class or you can use MoselSerializer class like below
#     """
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=150)
#     # to rename the field from unit_price to price I added source method
#     price = serializers.DecimalField(
#         max_digits=9, decimal_places=3, source='unit_price')
#     price_with_tax = serializers.SerializerMethodField(
#         method_name='calculate_tax')
#     collection = serializers.PrimaryKeyRelatedField(
#         queryset=Collection.objects.all()
#     )
#     collection_ref = serializers.StringRelatedField(source='collection')
#     nested_collection = CollectionSerializer(source='collection')
#     collectin_link = serializers.HyperlinkedRelatedField(
#         queryset=Collection.objects.all(), view_name='collections-details', source='collection'
#     )

#     def calculate_tax(self, product: Product):
#         return product.unit_price * Decimal(1.16)
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
                  'price_with_tax', 'slug', 'inventory', 'collection']
        #   ['collection_ref', 'nested_collection', 'collectin_link']

    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')
    # collection = serializers.PrimaryKeyRelatedField(
    #     queryset=Collection.objects.all()
    # )
    # collection_ref = serializers.StringRelatedField(source='collection')
    # nested_collection = CollectionSerializer(source='collection')
    # collectin_link = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(), view_name='collections-details', source='collection'
    # )

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.16)
