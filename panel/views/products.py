import os
import uuid
import shutil

from django.conf import settings
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.db.models import Count
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, View, DetailView

from panel.mixins import StaffRequiredMixin
from panel.forms import ProductForm
from products.models import Product
from categories.models import Category


def _save_image(image_file):
    storage_path = os.path.join(settings.BASE_DIR, 'static', 'images')
    os.makedirs(storage_path, exist_ok=True)
    fs = FileSystemStorage(location=storage_path)
    ext = os.path.splitext(image_file.name)[1]
    filename = fs.save(f"{uuid.uuid4()}{ext}", image_file)
    if not settings.DEBUG and settings.STATIC_ROOT:
        target_dir = os.path.join(settings.STATIC_ROOT, 'images')
        os.makedirs(target_dir, exist_ok=True)
        shutil.copy2(os.path.join(storage_path, filename), os.path.join(target_dir, filename))
    return f"images/{filename}"


class ProductListView(StaffRequiredMixin, ListView):
    model = Product
    template_name = 'panel/products/list.html'
    context_object_name = 'products'
    paginate_by = 20

    def get_queryset(self):
        qs = Product.objects.select_related('category__parent').filter(
            parent__isnull=True
        ).annotate(variant_count=Count('variants')).order_by('-id')
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
        ctx['categories'] = Category.objects.select_related('parent').order_by('parent__name', 'name')
        ctx['q'] = self.request.GET.get('q', '')
        ctx['selected_cat'] = self.request.GET.get('category', '')
        ctx['selected_status'] = self.request.GET.get('status', '')
        return ctx


class ProductVariantListView(StaffRequiredMixin, DetailView):
    model = Product
    template_name = 'panel/products/variants.html'
    context_object_name = 'main_product'

    def get_queryset(self):
        return Product.objects.select_related('category').filter(parent__isnull=True)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['variants'] = self.object.variants.select_related('category').order_by('id')
        return ctx


class ProductCreateView(StaffRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'panel/products/form.html'

    def get_success_url(self):
        parent_id = self.request.GET.get('parent')
        if parent_id:
            return reverse('panel:product-variants', kwargs={'pk': parent_id})
        return reverse('panel:product-list')

    def form_valid(self, form):
        instance = form.save(commit=False)
        parent_id = self.request.GET.get('parent')
        if parent_id:
            instance.parent_id = int(parent_id)
        image_file = form.cleaned_data.get('image_file')
        if image_file:
            instance.image_path = _save_image(image_file)
        instance.save()
        messages.success(self.request, "Mahsulot muvaffaqiyatli qo'shildi.")
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        parent_id = self.request.GET.get('parent')
        if parent_id:
            ctx['parent_product'] = get_object_or_404(Product, pk=parent_id, parent__isnull=True)
            ctx['title'] = f"Yangi variant: {ctx['parent_product'].name}"
        else:
            ctx['title'] = "Yangi mahsulot"
        return ctx


class ProductUpdateView(StaffRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'panel/products/form.html'

    def get_success_url(self):
        if self.object.parent_id:
            return reverse('panel:product-variants', kwargs={'pk': self.object.parent_id})
        return reverse('panel:product-list')

    def form_valid(self, form):
        instance = form.save(commit=False)
        image_file = form.cleaned_data.get('image_file')
        if image_file:
            instance.image_path = _save_image(image_file)
        instance.save()
        messages.success(self.request, "Mahsulot yangilandi.")
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = f"Tahrirlash: {self.object.name}"
        return ctx


class ProductDeleteView(StaffRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        parent_id = product.parent_id
        product.delete()
        messages.success(request, "Mahsulot o'chirildi.")
        if parent_id:
            return redirect('panel:product-variants', pk=parent_id)
        return redirect('panel:product-list')
