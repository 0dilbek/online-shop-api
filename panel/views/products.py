from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, View

from panel.mixins import StaffRequiredMixin
from panel.forms import ProductForm
from products.models import Product
from categories.models import Category


class ProductListView(StaffRequiredMixin, ListView):
    model = Product
    template_name = 'panel/products/list.html'
    context_object_name = 'products'
    paginate_by = 20

    def get_queryset(self):
        qs = Product.objects.select_related('category').order_by('-id')
        q = self.request.GET.get('q')
        cat = self.request.GET.get('category')
        status = self.request.GET.get('status')
        if q:
            qs = qs.filter(name__icontains=q)
        if cat:
            qs = qs.filter(category_id=cat)
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = Category.objects.all()
        ctx['q'] = self.request.GET.get('q', '')
        ctx['selected_cat'] = self.request.GET.get('category', '')
        ctx['selected_status'] = self.request.GET.get('status', '')
        return ctx


class ProductCreateView(StaffRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'panel/products/form.html'
    success_url = reverse_lazy('panel:product-list')

    def form_valid(self, form):
        messages.success(self.request, "Mahsulot muvaffaqiyatli qo'shildi.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = "Yangi mahsulot"
        return ctx


class ProductUpdateView(StaffRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'panel/products/form.html'
    success_url = reverse_lazy('panel:product-list')

    def form_valid(self, form):
        messages.success(self.request, "Mahsulot yangilandi.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = f"Tahrirlash: {self.object.name}"
        return ctx


class ProductDeleteView(StaffRequiredMixin, View):
    def post(self, request, pk):
        Product.objects.filter(pk=pk).delete()
        messages.success(request, "Mahsulot o'chirildi.")
        return redirect('panel:product-list')
