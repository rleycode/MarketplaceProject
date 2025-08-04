# admin_forms.py (создай рядом с admin.py)
from dal import autocomplete
from django import forms
from .models import Category, MarketplaceCategory

class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'ozon_category': autocomplete.ModelSelect2(url='ozon-category-autocomplete'),
            'wb_category': autocomplete.ModelSelect2(url='wb-category-autocomplete'),
        }
