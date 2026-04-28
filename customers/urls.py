from django.urls import path
from .views import (
    CustomerCreateView,
    CustomerLoginView,
    CustomerLogoutView,
    CustomerDetailView,
    CustomerByPhoneView,
    CustomerUpdateView,
)

urlpatterns = [
    path('customers', CustomerCreateView.as_view()),
    path('customers/login', CustomerLoginView.as_view()),
    path('customers/logout', CustomerLogoutView.as_view()),
    path('customers/by-phone', CustomerByPhoneView.as_view()),
    path('customers/<int:pk>', CustomerDetailView.as_view()),
    path('customers/<int:pk>/update', CustomerUpdateView.as_view()),
]
