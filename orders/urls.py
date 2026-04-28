from django.urls import path
from .views import OrderCreateView, OrderDetailView, OrderHistoryView

urlpatterns = [
    path('orders', OrderCreateView.as_view()),
    path('orders/history', OrderHistoryView.as_view()),
    path('orders/<int:pk>', OrderDetailView.as_view()),
]
