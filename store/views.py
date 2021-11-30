from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer


@api_view()
def products(request):
    query_set = Product.objects.all()
    serializer = ProductSerializer(query_set, many=True)
    return Response(serializer.data)


@api_view()
def product_list(request, id):
    product = get_object_or_404(Product, pk=id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)
