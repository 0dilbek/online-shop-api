from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Product, normalize_for_search
from .serializers import ProductSerializer


class ProductListView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        qs = Product.objects.select_related('category').all()
        category_id = self.request.query_params.get('category_id')
        is_top = self.request.query_params.get('is_top')
        search = self.request.query_params.get('search')

        if category_id:
            qs = qs.filter(category_id=category_id)
        if is_top is not None:
            qs = qs.filter(is_top=is_top.lower() == 'true')
        if search:
            qs = qs.filter(name_search__icontains=normalize_for_search(search))
        return qs


class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
