from django.contrib import admin
from .models import MarketplaceCategory, Category
from .admin_forms import CategoryAdminForm

@admin.register(MarketplaceCategory)
class MarketplaceCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "marketplace", "external_id", "name", "parent_external_id", "type_id")
    search_fields = ("name", "external_id")
    list_filter = ("marketplace",)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    list_display = ("id", "name", "ozon_category", "wb_category")
    search_fields = ("name",)
