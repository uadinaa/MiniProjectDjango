from django.shortcuts import render
from rest_framework import generics, permissions, filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product
from .serializers import ProductSerializer


class ProductFeedView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['seller', 'store', 'category']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'stock']

    def perform_create(self, serializer):
        """Создаёт продукт, но только если продавец имеет магазин"""
        seller = self.request.user.seller  # Получаем продавца из запроса
        store = serializer.validated_data.get("category").store  # Получаем магазин из категории продукта

        if store.seller != seller:
            raise PermissionDenied("Вы можете создавать продукты только для своего магазина.")

        serializer.save(seller=seller)

    def perform_update(self, serializer):
        """Обновление продукта (может делать только владелец)"""
        product = self.get_object()
        if product.seller != self.request.user.seller:
            raise PermissionDenied("Вы не можете редактировать этот товар.")
        serializer.save()

    def perform_destroy(self, instance):
        """Удаление продукта (может делать только владелец)"""
        if instance.seller != self.request.user.seller:
            raise PermissionDenied("Вы не можете удалить этот товар.")
        instance.delete()

