# from rest_framework import serializers
# import requests
# from django.core.files.base import ContentFile
# from django.contrib.auth import get_user_model
# from .models import Seller, Trader, Customer
#
# User = get_user_model()
#
#
# class UserRegistrationSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, min_length=6)
#
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'first_name', 'last_name', 'password', 'role']
#
#     def create(self, validated_data):
#         user = User.objects.create_user(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             first_name=validated_data['first_name'],
#             last_name=validated_data['last_name'],
#             password=validated_data['password'],
#             role=validated_data['role']
#         )
#         return user
#
#
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']  # Explicitly define fields
#
#
# class CustomerSerializer(serializers.ModelSerializer):
#     avatar_url = serializers.URLField(write_only=True, required=False)  # Accept URL input
#
#     class Meta:
#         model = Customer
#         fields = ["user", "avatar", "avatar_url"]
#
#     def create(self, validated_data):
#         avatar_url = validated_data.pop("avatar_url", None)  # Get URL from request
#         customer = super().create(validated_data)  # Create customer
#
#         if avatar_url:
#             response = requests.get(avatar_url)  # Download image
#             if response.status_code == 200:
#                 file_name = avatar_url.split("/")[-1]  # Extract filename
#                 customer.avatar.save(file_name, ContentFile(response.content), save=True)
#
#         return customer
#
#
# class SellerSerializer(serializers.ModelSerializer):
#     user = serializers.CharField(source="user.username")  # Show username instead of I
#     class Meta:
#         model = Seller
#         fields = ['id', 'user', 'company_name']
#
#
# class TraderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Trader
#         fields = '__all__'
#
#


from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Seller, Trader, Customer
import requests
from django.core.files.base import ContentFile

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password", "role"]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "role"]


class CustomerSerializer(serializers.ModelSerializer):
    avatar_url = serializers.URLField(write_only=True, required=False)

    class Meta:
        model = Customer
        fields = ["user", "avatar", "avatar_url"]

    def create(self, validated_data):
        avatar_url = validated_data.pop("avatar_url", None)
        customer = super().create(validated_data)
        if avatar_url:
            response = requests.get(avatar_url)
            if response.status_code == 200:
                file_name = avatar_url.split("/")[-1]
                customer.avatar.save(file_name, ContentFile(response.content), save=True)
        return customer


class SellerSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username")

    class Meta:
        model = Seller
        fields = ["id", "user", "company_name"]


class TraderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trader
        fields = "__all__"
