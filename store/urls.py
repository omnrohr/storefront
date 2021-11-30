from django.urls import path
from . import views


urlpatterns = [
    path('products/', views.products),
    path('products/<int:id>/', views.product_list),
]
