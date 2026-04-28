from orders.models import Order


def panel_globals(request):
    if request.user.is_authenticated and request.user.is_staff:
        return {'new_orders_count': Order.objects.filter(status=Order.STATUS_NEW).count()}
    return {}
