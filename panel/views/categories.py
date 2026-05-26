import os
import uuid
import shutil

from django.conf import settings
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, View

from panel.mixins import StaffRequiredMixin
from panel.forms import CategoryForm
from categories.models import Category


def build_flat_tree(categories, parent_id=None, depth=0):
    result = []
    for cat in sorted(categories, key=lambda c: c.id):
        if cat.parent_id == parent_id:
            result.append((cat, depth))
            result.extend(build_flat_tree(categories, cat.id, depth + 1))
    return result


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


class CategoryListView(StaffRequiredMixin, ListView):
    template_name = 'panel/categories/list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.annotate(product_count=Count('products')).select_related('parent')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        all_cats = list(ctx['categories'])
        ctx['tree_categories'] = build_flat_tree(all_cats)
        return ctx


class CategoryCreateView(StaffRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'panel/categories/form.html'
    success_url = reverse_lazy('panel:category-list')

    def form_valid(self, form):
        instance = form.save(commit=False)
        image_file = form.cleaned_data.get('image_file')
        if image_file:
            instance.image_path = _save_image(image_file)
        instance.save()
        messages.success(self.request, "Kategoriya qo'shildi.")
        return redirect(self.success_url)

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
        instance = form.save(commit=False)
        image_file = form.cleaned_data.get('image_file')
        if image_file:
            instance.image_path = _save_image(image_file)
        instance.save()
        messages.success(self.request, "Kategoriya yangilandi.")
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = f"Tahrirlash: {self.object.name}"
        return ctx


class CategoryDeleteView(StaffRequiredMixin, View):
    def post(self, request, pk):
        cat = Category.objects.filter(pk=pk).first()
        if cat:
            if cat.children.exists():
                messages.error(request, "Bu kategoriyada ichki kategoriyalar bor. Avval ularni o'chiring.")
                return redirect('panel:category-list')
            cat.delete()
            messages.success(request, "Kategoriya o'chirildi.")
        return redirect('panel:category-list')
