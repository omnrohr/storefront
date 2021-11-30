from django.db.models.query import QuerySet
from django.http.response import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer


@api_view(['GET', 'POST'])
def products(request):
    if request.method == 'GET':
        # I added select related to call the related coloumn in product model with porduct in same time to prevent make
        #  a single query to database when calling the collection name. review the serilaizer in prodcut class
        query_set = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(
            query_set, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PATCH', 'PUT'])
def product_list(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == 'GET':
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = ProductSerializer(instance=product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
    elif request.method == 'PUT':
        serializer = ProductSerializer(instance=product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view()
def collection_details(request, pk):
    return Response('ok')
