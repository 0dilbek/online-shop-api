from rest_framework import serializers
from .models import Cart, CartItem


class CartItemCreateSerializer(serializers.Serializer):
    session_id = serializers.CharField()
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class CartItemUpdateSerializer(serializers.Serializer):
    session_id = serializers.CharField()
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=0)


class CartItemOutSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    quantity = serializers.IntegerField()
    unit_price = serializers.IntegerField()
    total_price = serializers.IntegerField()
    image = serializers.CharField(allow_null=True)


class CartOutSerializer(serializers.Serializer):
    id = serializers.IntegerField(allow_null=True)
    session_id = serializers.CharField()
    items = CartItemOutSerializer(many=True)
    total_price = serializers.IntegerField()
