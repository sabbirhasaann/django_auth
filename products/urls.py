from django.urls import path
from .views import ProductListCreateView, ProductView, ProductViewSet

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/create/', ProductView.as_view(), name='create-product'),
    path('products/<int:pk>/retrieve/', ProductViewSet.as_view({
        'get': 'retrieve'
    }), name='retrieve - products'),
    path('products/<int:pk>/publish/', ProductViewSet.as_view({
        'post': 'publish'
    }), name='publish-product'),
]
