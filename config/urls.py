from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def root(request):
    return Response({'message': 'Online shop API is running'})


from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('panel/', include('panel.urls')),
    path('', root),
    # Swagger
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # API endpoints
    path('api/v1/', include('categories.urls')),
    path('api/v1/', include('products.urls')),
    path('api/v1/', include('customers.urls')),
    path('api/v1/', include('orders.urls')),
    path('api/v1/', include('cart.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
