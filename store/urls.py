from django.urls import path
from django.urls.conf import include
from . import views
from rest_framework.routers import SimpleRouter
router = SimpleRouter()
router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('products/', views.ProductList.as_view()),
    # path('products/<int:pk>/', views.ProductDetail.as_view()),
    # path('collections/', views.CollectionList.as_view()),
    # path('collections/<int:pk>/', views.CollectionDetails.as_view(),
    #      name='collections-details'),
]
