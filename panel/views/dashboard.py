from django.views.generic import TemplateView
from django.db.models import Sum
from django.utils import timezone

from panel.mixins import StaffRequiredMixin
from orders.models import Order
from products.models import Product
from customers.models import Customer
from categories.models import Category


class DashboardView(StaffRequiredMixin, TemplateView):
    template_name = 'panel/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = timezone.now().date()

        status_counts = {}
        for s, _ in Order.STATUS_CHOICES:
            status_counts[s] = Order.objects.filter(status=s).count()

        ctx.update({
            'orders_today': Order.objects.filter(created_at__date=today).count(),
            'total_revenue': Order.objects.filter(
                status=Order.STATUS_COMPLETED
            ).aggregate(t=Sum('total_price'))['t'] or 0,
            'total_customers': Customer.objects.count(),
            'active_products': Product.objects.filter(status=Product.STATUS_ACTIVE).count(),
            'recent_orders': Order.objects.select_related('customer').order_by('-created_at')[:8],
            'status_counts': status_counts,
        })
        return ctx
