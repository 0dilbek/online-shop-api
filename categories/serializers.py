from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'unit_type', 'image', 'parent_id', 'children']

    def get_image(self, obj):
        return obj.image

    def get_children(self, obj):
        kids = obj.children.all()
        if not kids:
            return []
        return CategorySerializer(kids, many=True).data
