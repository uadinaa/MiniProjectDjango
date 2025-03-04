from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    seller_name = serializers.ReadOnlyField(source="seller.user.username")  # Показываем имя продавца
    store_name = serializers.ReadOnlyField(source="category.store.name")  # Показываем магазин

    class Meta:
        model = Product
        fields = '__all__'