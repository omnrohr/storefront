from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer


class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitems.count() > 0:
            return Response({
                'error': 'This item is included in some orders, we apologize for not being able to delete it'
            }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(
        products_count=Count('products')).all()
    serializer_class = CollectionSerializer


class CollectionDetails(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.annotate(
        products_count=Count('products'))
    serializer_class = CollectionSerializer
    # def get(self, request, pk):
    #     collection = get_object_or_404(Collection.objects.annotate(
    #         products_count=Count('products')), pk=pk)
    #     serializer = CollectionSerializer(
    #         collection, context={'request': request})
    #     return Response(serializer.data)

    # def patch(self, request, pk):
    #     collection = get_object_or_404(Collection.objects.annotate(
    #         products_count=Count('products')), pk=pk)
    #     serializer = CollectionSerializer(
    #         instance=collection, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    # def put(self, request, pk):
    #     collection = get_object_or_404(Collection.objects.annotate(
    #         products_count=Count('products')), pk=pk)
    #     serializer = CollectionSerializer(collection, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, pk):
        collection = get_object_or_404(Collection.objects.annotate(
            products_count=Count('products')), pk=pk)
        if collection.products.count() > 0:
            return Response({
                'error': 'This collection is included in some items, we apologize for not being able to delete it'
            }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
