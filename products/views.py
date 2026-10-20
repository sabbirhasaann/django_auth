from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from .models import Product
from .serializers import ProductSerializer, ProductCreateSerializer
from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ModelViewSet

class ProductListCreateView(generics.ListCreateAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductView(APIView):

    @extend_schema(
        summary="Create a product",
        description="This contains product informations",
        request=ProductCreateSerializer,
        responses={
            200: ProductSerializer,
        }

    )
    def post(self, request):
        pass

class ProductViewSet(ModelViewSet):

    @extend_schema(
        summary="Retrieve a product",
        responses=ProductSerializer,
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(
            request,
            *args,
            **kwargs,
        )
