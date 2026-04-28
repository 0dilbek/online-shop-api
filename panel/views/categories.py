from django.contrib import messages
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, View

from panel.mixins import StaffRequiredMixin
from panel.forms import CategoryForm
from categories.models import Category


class CategoryListView(StaffRequiredMixin, ListView):
    template_name = 'panel/categories/list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.annotate(product_count=Count('products')).order_by('id')


class CategoryCreateView(StaffRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'panel/categories/form.html'
    success_url = reverse_lazy('panel:category-list')

    def form_valid(self, form):
        messages.success(self.request, "Kategoriya qo'shildi.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = "Yangi kategoriya"
        return ctx


class CategoryUpdateView(StaffRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'panel/categories/form.html'
    success_url = reverse_lazy('panel:category-list')

    def form_valid(self, form):
        messages.success(self.request, "Kategoriya yangilandi.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = f"Tahrirlash: {self.object.name}"
        return ctx


class CategoryDeleteView(StaffRequiredMixin, View):
    def post(self, request, pk):
        Category.objects.filter(pk=pk).delete()
        messages.success(request, "Kategoriya o'chirildi.")
        return redirect('panel:category-list')
