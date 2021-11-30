from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view()
def products(request):
    return Response('ok for products')


@api_view()
def prducts_list(requst, id):
    return Response(f'this {id} is the first product')
