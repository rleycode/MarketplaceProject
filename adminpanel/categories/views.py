# views.py
from dal import autocomplete
from .models import MarketplaceCategory

class OzonCategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = MarketplaceCategory.objects.filter(marketplace='OZON')  # фильтруем, если нужно
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs

class WbCategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = MarketplaceCategory.objects.filter(marketplace='WB')
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs
