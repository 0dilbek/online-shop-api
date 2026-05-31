from rest_framework import serializers
from .models import Product
from categories.serializers import CategorySerializer


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    categories = CategorySerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'description', 'status', 'is_top', 'image', 'category', 'categories']

    def get_image(self, obj):
        return obj.image

    def get_category(self, obj):
        category = next(iter(obj.categories.all()), None)
        if not category:
            return None
        return CategorySerializer(category).data


class VariantSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'description', 'status', 'image']

    def get_image(self, obj):
        return obj.image


class ProductDetailSerializer(ProductSerializer):
    variants = VariantSerializer(many=True, read_only=True)

    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields + ['variants']
