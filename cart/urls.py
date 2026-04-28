from django.urls import path
from .views import CartView, CartItemAddView, CartItemUpdateView, CartItemDeleteView

urlpatterns = [
    path('cart', CartView.as_view()),
    path('cart/items', CartItemAddView.as_view()),
    path('cart/items/update', CartItemUpdateView.as_view()),
    path('cart/items/<int:item_id>', CartItemDeleteView.as_view()),
]
