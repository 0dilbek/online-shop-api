from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError, NotFound

from .models import Cart, CartItem
from .serializers import CartItemCreateSerializer, CartItemUpdateSerializer
from products.models import Product


def _build_cart_response(cart, session_id):
    if not cart:
        return {'id': None, 'session_id': session_id, 'items': [], 'total_price': 0}

    items = []
    total_price = 0
    for item in cart.items.select_related('product').all():
        line_total = item.unit_price * item.quantity
        total_price += line_total
        items.append({
            'id': item.id,
            'product_id': item.product_id,
            'product_name': item.product.name if item.product else '',
            'quantity': item.quantity,
            'unit_price': item.unit_price,
            'total_price': line_total,
            'image': item.image,
        })

    return {'id': cart.id, 'session_id': cart.session_id or session_id, 'items': items, 'total_price': total_price}


def _get_or_create_cart(session_id):
    cart = Cart.objects.filter(session_id=session_id, status=Cart.STATUS_OPEN).first()
    if not cart:
        cart = Cart.objects.create(session_id=session_id, status=Cart.STATUS_OPEN)
    return cart


class CartView(APIView):
    def get(self, request):
        session_id = request.query_params.get('session_id')
        if not session_id:
            raise ValidationError("session_id is required")
        cart = Cart.objects.filter(session_id=session_id, status=Cart.STATUS_OPEN).first()
        return Response(_build_cart_response(cart, session_id))

    def delete(self, request):
        session_id = request.query_params.get('session_id')
        if not session_id:
            raise ValidationError("session_id is required")
        cart = Cart.objects.filter(session_id=session_id, status=Cart.STATUS_OPEN).first()
        if not cart:
            return Response({'id': None, 'session_id': session_id, 'items': [], 'total_price': 0})
        cart.items.all().delete()
        cart.refresh_from_db()
        return Response(_build_cart_response(cart, session_id))


class CartItemAddView(APIView):
    def post(self, request):
        serializer = CartItemCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        product = Product.objects.filter(id=data['product_id'], status=Product.STATUS_ACTIVE).first()
        if not product:
            raise ValidationError("Product not found or inactive")

        cart = _get_or_create_cart(data['session_id'])
        item = CartItem.objects.filter(cart=cart, product_id=data['product_id']).first()

        if item:
            item.quantity = data['quantity']
            item.unit_price = product.price
            item.save()
        else:
            CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=data['quantity'],
                unit_price=product.price,
            )

        cart.refresh_from_db()
        return Response(_build_cart_response(cart, data['session_id']))


class CartItemUpdateView(APIView):
    def patch(self, request):
        serializer = CartItemUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        cart = Cart.objects.filter(session_id=data['session_id'], status=Cart.STATUS_OPEN).first()
        if not cart:
            raise NotFound("Cart not found")

        item = CartItem.objects.filter(cart=cart, product_id=data['product_id']).first()
        if not item:
            raise NotFound("Cart item not found")

        if data['quantity'] == 0:
            item.delete()
        else:
            item.quantity = data['quantity']
            item.save()

        cart.refresh_from_db()
        return Response(_build_cart_response(cart, data['session_id']))


class CartItemDeleteView(APIView):
    def delete(self, request, item_id):
        session_id = request.query_params.get('session_id')
        if not session_id:
            raise ValidationError("session_id is required")

        cart = Cart.objects.filter(session_id=session_id, status=Cart.STATUS_OPEN).first()
        if not cart:
            raise NotFound("Cart not found")

        item = CartItem.objects.filter(id=item_id, cart=cart).first()
        if not item:
            raise NotFound("Cart item not found")

        item.delete()
        cart.refresh_from_db()
        return Response(_build_cart_response(cart, session_id))
