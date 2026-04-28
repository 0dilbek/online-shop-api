from django.views.generic import ListView, DetailView

from panel.mixins import StaffRequiredMixin
from customers.models import Customer


class CustomerListView(StaffRequiredMixin, ListView):
    model = Customer
    template_name = 'panel/customers/list.html'
    context_object_name = 'customers'
    paginate_by = 25

    def get_queryset(self):
        qs = Customer.objects.order_by('-created_at')
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(full_name__icontains=q) | qs.filter(phone__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['q'] = self.request.GET.get('q', '')
        return ctx


class CustomerDetailView(StaffRequiredMixin, DetailView):
    model = Customer
    template_name = 'panel/customers/detail.html'
    context_object_name = 'customer'

    def get_queryset(self):
        return Customer.objects.prefetch_related('orders__items')
