from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer


class ProductList(APIView):
    def get(self, request):
        query_set = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(
            query_set, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class ProductDetail(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(
            product, context={'request': request})
        return Response(serializer.data)

    def patch(self, request):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(
            instance=product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)

    def put(self, request):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(
            instance=product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request):
        product = get_object_or_404(Product, pk=id)
        if product.orderitems.count() > 0:
            return Response({
                'error': 'This item is included in some orders, we apologize for not being able to delete it'
            }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionList(APIView):
    def get(self, request):
        query_set = Collection.objects.annotate(
            products_count=Count('products')).all()
        serializer = CollectionSerializer(query_set, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CollectionDetails(APIView):
    def get(self, request, pk):
        collection = get_object_or_404(Collection.objects.annotate(
            products_count=Count('products')), pk=pk)
        serializer = CollectionSerializer(
            collection, context={'request': request})
        return Response(serializer.data)

    def patch(self, request, pk):
        collection = get_object_or_404(Collection.objects.annotate(
            products_count=Count('products')), pk=pk)
        serializer = CollectionSerializer(
            instance=collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def put(self, request, pk):
        collection = get_object_or_404(Collection.objects.annotate(
            products_count=Count('products')), pk=pk)
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, pk):
        collection = get_object_or_404(Collection.objects.annotate(
            products_count=Count('products')), pk=pk)
        if collection.products.count() > 0:
            return Response({
                'error': 'This collection is included in some items, we apologize for not being able to delete it'
            }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
