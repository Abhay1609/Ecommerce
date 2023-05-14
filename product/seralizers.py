from rest_framework import serializers
from .models import *
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=(
            "id",
            "name",
            "get_absolute_urls",
            "description",
            "price",
            "get_image",
            "get_thumbnail"
        )


class CategorySerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "get_absolute_urls",
            "product",

        )

class AddProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=["id","name","category","description","price","image"]
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cart
        fields=["user"]

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=["user","status"]
class ProductCartSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductInCart
        fields=["cart_id","name","quantity"]
