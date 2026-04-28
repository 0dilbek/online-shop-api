from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def root(request):
    return Response({'message': 'Online shop API is running'})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('panel/', include('panel.urls')),
    path('', root),
    path('api/v1/', include('categories.urls')),
    path('api/v1/', include('products.urls')),
    path('api/v1/', include('customers.urls')),
    path('api/v1/', include('orders.urls')),
    path('api/v1/', include('cart.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
