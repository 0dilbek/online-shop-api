from rest_framework import serializers
from .models import Product
from categories.serializers import CategorySerializer


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'description', 'status', 'is_top', 'image', 'category']

    def get_image(self, obj):
        return obj.image
