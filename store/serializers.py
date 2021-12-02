from decimal import Decimal
from rest_framework import serializers
from store.models import Cart, CartItem, Product, Collection, Review, OrderItem


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


class SimpleProductSerializer(serializers.ModelSerializer):
    # I create this serilazer to retreve the data needed for cart items
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    total_price = serializers.SerializerMethodField(
        method_name='get_total_price')

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    cart_total = serializers.SerializerMethodField(
        method_name='get_cart_total')

    def get_cart_total(self, cart=Cart):
        cart_total = sum([item.product.unit_price *
                          item.quantity for item in cart.items.all()])
        return cart_total

    class Meta:
        model = Cart
        fields = ['id', 'items', 'cart_total']


class AddCartItemsSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No product with the given ID')
        return value

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        try:
            cart_item = CartItem.objects.get(
                cart_id=cart_id, product_id=product_id)
            # if item exists that mean you need to update the quantity
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            # if item not exist you need to create an item
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data)
        return self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']
