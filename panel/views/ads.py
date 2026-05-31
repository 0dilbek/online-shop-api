import os
import shutil
import uuid

from django.conf import settings
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, View

from ads.models import Advertisement
from panel.forms import AdvertisementForm
from panel.mixins import StaffRequiredMixin


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


class AdvertisementListView(StaffRequiredMixin, ListView):
    model = Advertisement
    template_name = 'panel/ads/list.html'
    context_object_name = 'ads'
    paginate_by = 20

    def get_queryset(self):
        qs = Advertisement.objects.all()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(title__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['q'] = self.request.GET.get('q', '')
        return ctx


class AdvertisementCreateView(StaffRequiredMixin, CreateView):
    model = Advertisement
    form_class = AdvertisementForm
    template_name = 'panel/ads/form.html'
    success_url = reverse_lazy('panel:ad-list')

    def form_valid(self, form):
        instance = form.save(commit=False)
        image_file = form.cleaned_data.get('image_file')
        if image_file:
            instance.image_path = _save_image(image_file)
        instance.save()
        messages.success(self.request, "Reklama qo'shildi.")
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = "Yangi reklama"
        return ctx


class AdvertisementUpdateView(StaffRequiredMixin, UpdateView):
    model = Advertisement
    form_class = AdvertisementForm
    template_name = 'panel/ads/form.html'
    success_url = reverse_lazy('panel:ad-list')

    def form_valid(self, form):
        instance = form.save(commit=False)
        image_file = form.cleaned_data.get('image_file')
        if image_file:
            instance.image_path = _save_image(image_file)
        instance.save()
        messages.success(self.request, "Reklama yangilandi.")
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = f"Tahrirlash: {self.object.title}"
        return ctx


class AdvertisementDeleteView(StaffRequiredMixin, View):
    def post(self, request, pk):
        ad = get_object_or_404(Advertisement, pk=pk)
        ad.delete()
        messages.success(request, "Reklama o'chirildi.")
        return redirect('panel:ad-list')
