from django.urls import path
from . import views


urlpatterns = [
    path('products/', views.products),
    path('products/<int:id>/', views.product_list),
    path('collections/', views.collection_list),
    path('collections/<int:pk>/', views.collection_details,
         name='collections-details'),

]
