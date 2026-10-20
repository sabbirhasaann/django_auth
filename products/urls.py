from django.urls import path
from .views import ProductListCreateView, ProductView

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/create/', ProductView.as_view(), name='create-product')
]
