from rest_framework import status
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError, NotFound

from .models import Order, OrderItem
from .serializers import OrderCreateSerializer, OrderSerializer
from products.models import Product
from customers.models import Customer


class OrderCreateView(APIView):
    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        customer = None
        if data.get('customer_id'):
            try:
                customer = Customer.objects.get(pk=data['customer_id'])
            except Customer.DoesNotExist:
                raise ValidationError("Customer not found")

        name = data.get('customer_name') or (customer.full_name if customer else None)
        phone = data.get('customer_phone') or (customer.phone if customer else None)
        address = data.get('address') or (customer.default_address if customer else None)

        if not name or not phone or not address:
            raise ValidationError("Customer name, phone and address are required")

        product_ids = {item['product_id'] for item in data['items']}
        products = Product.objects.filter(id__in=product_ids, status=Product.STATUS_ACTIVE)
        products_map = {p.id: p for p in products}

        if len(products_map) != len(product_ids):
            raise ValidationError("One or more products not found or inactive")

        order = Order.objects.create(
            customer=customer,
            customer_name=name,
            customer_phone=phone,
            address=address,
            status=Order.STATUS_NEW,
            total_price=0,
        )

        total_price = 0
        for item in data['items']:
            product = products_map[item['product_id']]
            line_total = product.price * item['quantity']
            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                unit_price=product.price,
                quantity=item['quantity'],
                total_price=line_total,
            )
            total_price += line_total

        order.total_price = total_price
        order.save()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderDetailView(RetrieveAPIView):
    queryset = Order.objects.prefetch_related('items__product').all()
    serializer_class = OrderSerializer


class OrderHistoryView(ListAPIView):
    serializer_class = OrderSerializer
    pagination_class = None

    def get_queryset(self):
        customer_id = self.request.query_params.get('customer_id')
        if not customer_id:
            raise ValidationError("customer_id query param is required")
        return Order.objects.filter(customer_id=customer_id).prefetch_related('items__product')
