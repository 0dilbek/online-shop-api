from django import forms
from ads.models import Advertisement
from categories.models import Category
from products.models import Product


_input = 'w-full bg-[#f4f6f9] rounded-xl px-4 py-3 text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#00964b] border-0'
_select = 'w-full bg-[#f4f6f9] rounded-xl px-4 py-3 text-gray-800 focus:outline-none focus:ring-2 focus:ring-[#00964b] border-0'


class CategoryForm(forms.ModelForm):
    image_file = forms.ImageField(
        required=False,
        label="Rasm yuklash (ixtiyoriy)",
        widget=forms.FileInput(attrs={'class': _input, 'accept': 'image/*'})
    )

    class Meta:
        model = Category
        fields = ['name', 'parent', 'unit_type', 'image_path']
        widgets = {
            'name': forms.TextInput(attrs={'class': _input, 'placeholder': 'Kategoriya nomi'}),
            'parent': forms.Select(attrs={'class': _select}),
            'unit_type': forms.Select(
                choices=[('piece', 'Dona (piece)'), ('weight', 'Vazn (weight)')],
                attrs={'class': _select},
            ),
            'image_path': forms.TextInput(attrs={'class': _input, 'placeholder': 'Rasm yo\'li yoki URL (ixtiyoriy)'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].required = False
        self.fields['parent'].empty_label = 'Yuqori daraja (parent yo\'q)'
        self.fields['parent'].label = 'Yuqori kategoriya'
        self.fields['unit_type'].required = False
        self.fields['image_path'].required = False
        self.fields['image_file'].required = False
        self.fields['image_path'].label = 'Rasm URL (ixtiyoriy)'
        self.fields['parent'].queryset = Category.objects.filter(
            parent__isnull=True
        ).order_by('name')


class ProductForm(forms.ModelForm):
    image_file = forms.ImageField(
        required=False,
        label="Rasm yuklash (ixtiyoriy)",
        widget=forms.FileInput(attrs={'class': _input, 'accept': 'image/*'})
    )

    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'categories', 'status', 'is_top', 'image_path']
        widgets = {
            'name': forms.TextInput(attrs={'class': _input, 'placeholder': 'Mahsulot nomi'}),
            'price': forms.NumberInput(attrs={'class': _input, 'placeholder': 'Narx (so\'m)'}),
            'description': forms.Textarea(attrs={'class': _input, 'rows': 3, 'placeholder': 'Tavsif (ixtiyoriy)'}),
            'categories': forms.SelectMultiple(attrs={'class': _select, 'size': 10}),
            'status': forms.Select(
                choices=[('active', 'Faol'), ('inactive', 'Nofaol')],
                attrs={'class': _select},
            ),
            'is_top': forms.CheckboxInput(attrs={'class': 'w-5 h-5 rounded accent-[#00964b]'}),
            'image_path': forms.TextInput(attrs={'class': _input, 'placeholder': 'Rasm yo\'li yoki URL (ixtiyoriy)'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].required = False
        self.fields['image_path'].required = False
        self.fields['image_file'].required = False
        self.fields['description'].label = "Tavsif (ixtiyoriy)"
        self.fields['image_path'].label = "Rasm URL (ixtiyoriy)"
        self.fields['categories'].label = "Kategoriyalar"
        self.fields['categories'].queryset = Category.objects.select_related('parent').order_by('parent__name', 'name')


class AdvertisementForm(forms.ModelForm):
    image_file = forms.ImageField(
        required=False,
        label="Rasm yuklash (ixtiyoriy)",
        widget=forms.FileInput(attrs={'class': _input, 'accept': 'image/*'})
    )

    class Meta:
        model = Advertisement
        fields = ['title', 'text', 'image_path']
        widgets = {
            'title': forms.TextInput(attrs={'class': _input, 'placeholder': 'Reklama sarlavhasi'}),
            'text': forms.Textarea(attrs={'class': _input, 'rows': 10, 'placeholder': 'Markdown matn'}),
            'image_path': forms.TextInput(attrs={'class': _input, 'placeholder': 'Rasm yo\'li yoki URL (ixtiyoriy)'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image_path'].required = False
        self.fields['image_file'].required = False
        self.fields['image_path'].label = "Rasm URL (ixtiyoriy)"
        self.fields['text'].label = "Matn"

    def clean_image_path(self):
        image_path = self.cleaned_data.get('image_path')
        return image_path.strip() if image_path else image_path
