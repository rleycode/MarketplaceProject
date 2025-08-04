# products/admin.py

from django.contrib import admin
from .models import Product, Brand, Media, Fitment


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'brand', 'common_sku', 'activity')
    list_filter = ('activity', 'brand', 'type')
    search_fields = ('name', 'used_sku', 'common_sku', 'part_number', 'id_1c')
    autocomplete_fields = ('brand', 'media', 'fitment', 'type')  # удобный выпадающий поиск
    list_editable = ('activity',)
    readonly_fields = ('ozon_update', 'wb_update')


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('id',)
    search_fields = ('id',)  # если появятся другие поля — добавим


@admin.register(Fitment)
class FitmentAdmin(admin.ModelAdmin):
    list_display = ('id',)
    search_fields = ('id',)

