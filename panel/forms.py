from django import forms
from categories.models import Category
from products.models import Product


_input = 'w-full bg-[#f4f6f9] rounded-xl px-4 py-3 text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#00964b] border-0'
_select = 'w-full bg-[#f4f6f9] rounded-xl px-4 py-3 text-gray-800 focus:outline-none focus:ring-2 focus:ring-[#00964b] border-0'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'unit_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': _input, 'placeholder': 'Kategoriya nomi'}),
            'unit_type': forms.Select(
                choices=[('', 'Birlikni tanlang'), ('piece', 'Dona (piece)'), ('weight', 'Vazn (weight)')],
                attrs={'class': _select},
            ),
        }


class ProductForm(forms.ModelForm):
    image_file = forms.ImageField(
        required=False,
        label="Rasm yuklash (ixtiyoriy)",
        widget=forms.FileInput(attrs={'class': _input, 'accept': 'image/*'})
    )

    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'category', 'status', 'is_top', 'image_path']
        widgets = {
            'name': forms.TextInput(attrs={'class': _input, 'placeholder': 'Mahsulot nomi'}),
            'price': forms.NumberInput(attrs={'class': _input, 'placeholder': 'Narx (so\'m)'}),
            'description': forms.Textarea(attrs={'class': _input, 'rows': 3, 'placeholder': 'Tavsif (ixtiyoriy)'}),
            'category': forms.Select(attrs={'class': _select}),
            'status': forms.Select(
                choices=[('active', 'Faol'), ('inactive', 'Nofaol')],
                attrs={'class': _select},
            ),
            'is_top': forms.CheckboxInput(attrs={'class': 'w-5 h-5 rounded accent-[#00964b]'}),
            'image_path': forms.URLInput(attrs={'class': _input, 'placeholder': 'Yoki rasm URL manzilini kiriting (ixtiyoriy)'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].required = False
        self.fields['image_path'].required = False
        self.fields['image_file'].required = False
        self.fields['description'].label = "Tavsif (ixtiyoriy)"
        self.fields['image_path'].label = "Rasm URL (ixtiyoriy)"
