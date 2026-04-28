from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, ValidationError

from .models import Customer
from .serializers import (
    CustomerSerializer,
    CustomerCreateSerializer,
    CustomerUpdateSerializer,
    CustomerLoginSerializer,
)


class CustomerCreateView(CreateAPIView):
    serializer_class = CustomerCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer = serializer.save()
        return Response(CustomerSerializer(customer).data, status=status.HTTP_201_CREATED)


class CustomerLoginView(APIView):
    def post(self, request):
        serializer = CustomerLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        password = serializer.validated_data['password']

        try:
            customer = Customer.objects.get(phone=phone)
        except Customer.DoesNotExist:
            raise ValidationError("Phone or password incorrect")

        if not customer.verify_password(password):
            raise ValidationError("Phone or password incorrect")

        return Response({
            'status': 'success',
            'message': 'Login successful',
            'customer': CustomerSerializer(customer).data,
        })


class CustomerLogoutView(APIView):
    def post(self, request):
        return Response({'status': 'success', 'message': 'Logout successful'})


class CustomerDetailView(RetrieveAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CustomerByPhoneView(APIView):
    def get(self, request):
        phone = request.query_params.get('phone')
        if not phone:
            raise ValidationError("phone query param is required")
        try:
            customer = Customer.objects.get(phone=phone)
        except Customer.DoesNotExist:
            raise NotFound("Customer not found")
        return Response(CustomerSerializer(customer).data)


class CustomerUpdateView(UpdateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerUpdateSerializer
    http_method_names = ['patch']

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        customer = serializer.save()
        return Response(CustomerSerializer(customer).data)
