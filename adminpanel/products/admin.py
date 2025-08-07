from django.contrib import admin
from .models import (
    AlembicVersion,
    BrandAliases,
    Brands,
    Categories,
    Characteristics,
    Fitment,
    MarketplaceCategories,
    Media,
    Oem,
    OzonFitment,
    Prices,
    Products,
)


@admin.register(AlembicVersion)
class AlembicVersionAdmin(admin.ModelAdmin):
    list_display = ('version_num',)


@admin.register(BrandAliases)
class BrandAliasesAdmin(admin.ModelAdmin):
    list_display = ('brand', 'marketplace', 'alias_name')
    list_filter = ('marketplace',)


@admin.register(Brands)
class BrandsAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['name', 'ozon_category', 'wb_category']
    autocomplete_fields = ['ozon_category', 'wb_category']

@admin.register(Characteristics)
class CharacteristicsAdmin(admin.ModelAdmin):
    list_display = ('weight', 'height', 'width', 'length', 'country')


@admin.register(Fitment)
class FitmentAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'body', 'year_1', 'year_2')


@admin.register(MarketplaceCategories)
class MarketplaceCategoriesAdmin(admin.ModelAdmin):
    list_display = ('marketplace', 'external_id', 'name', 'updated_at')
    search_fields = ('name', 'external_id', 'marketplace')


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('image_1', 'video', 'certificate')


@admin.register(Oem)
class OemAdmin(admin.ModelAdmin):
    list_display = ('oem_brand', 'oem_sku', 'cross_brand', 'cross_sku')
    search_fields = ('oem_sku', 'cross_sku')


@admin.register(OzonFitment)
class OzonFitmentAdmin(admin.ModelAdmin):
    list_display = ('ozon_sku', 'make', 'model', 'modification')
    search_fields = ('ozon_sku',)


@admin.register(Prices)
class PricesAdmin(admin.ModelAdmin):
    list_display = ('purchase_price', 'price_ozon', 'profit', 'vat')


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'ozon_sku', 'wb_id', 'yandex_id')
    search_fields = ('name', 'ozon_sku', 'wb_id', 'yandex_id')
    list_filter = ('brand', 'type')
