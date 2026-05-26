from rest_framework.generics import ListAPIView
from .models import Category
from .serializers import CategorySerializer


class CategoryListView(ListAPIView):
    serializer_class = CategorySerializer
    pagination_class = None

    def get_queryset(self):
        return Category.objects.filter(parent__isnull=True).prefetch_related(
            'children', 'children__children'
        ).order_by('id')
