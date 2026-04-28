from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View

from panel.mixins import StaffRequiredMixin
from orders.models import Order


class OrderListView(StaffRequiredMixin, ListView):
    model = Order
    template_name = 'panel/orders/list.html'
    context_object_name = 'orders'
    paginate_by = 25

    def get_queryset(self):
        qs = Order.objects.select_related('customer').order_by('-created_at')
        status = self.request.GET.get('status')
        q = self.request.GET.get('q')
        if status:
            qs = qs.filter(status=status)
        if q:
            qs = qs.filter(customer_name__icontains=q) | qs.filter(customer_phone__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['status_choices'] = Order.STATUS_CHOICES
        ctx['selected_status'] = self.request.GET.get('status', '')
        ctx['q'] = self.request.GET.get('q', '')
        return ctx


class OrderDetailView(StaffRequiredMixin, DetailView):
    model = Order
    template_name = 'panel/orders/detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        return Order.objects.prefetch_related('items__product').select_related('customer')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['status_choices'] = Order.STATUS_CHOICES
        return ctx


class OrderStatusUpdateView(StaffRequiredMixin, View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        new_status = request.POST.get('status')
        valid = [s for s, _ in Order.STATUS_CHOICES]
        if new_status in valid:
            order.status = new_status
            order.save()
            messages.success(request, f"Status o'zgartirildi: {order.get_status_display()}")
        return redirect('panel:order-detail', pk=pk)
