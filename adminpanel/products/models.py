from django.db import models
from categories.models import Category
from django.utils import timezone


class Brand(models.Model):
    class Meta:
        db_table = 'brendy'

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    # ... другие поля ...


class Media(models.Model):
    class Meta:
        db_table = 'media'

    id = models.AutoField(primary_key=True)
    # ... другие поля ...


class Fitment(models.Model):
    class Meta:
        db_table = 'fitment_-_primenyaemost'

    id = models.AutoField(primary_key=True)
    # ... другие поля ...

class Product(models.Model):
    class Meta:
        db_table = 'nomenklatura'

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    brand = models.ForeignKey(
        Brand,
        to_field='name',
        db_column='brand',
        on_delete=models.SET_NULL,
        null=True,
        related_name='products'
    )
    used_sku = models.CharField(max_length=255, blank=True, null=True)
    sku_1 = models.CharField(max_length=255, blank=True, null=True)
    sku_2 = models.CharField(max_length=255, blank=True, null=True)
    common_sku = models.CharField(max_length=255, blank=True, null=True)
    ozon_sku = models.CharField(max_length=255, blank=True, null=True)
    part_number = models.CharField(max_length=255, blank=True, null=True)
    id_1c = models.CharField(max_length=255, blank=True, null=True)
    id_mp = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    wb_sku = models.CharField(max_length=255, blank=True, null=True)
    ozon_update = models.DateTimeField(default=timezone.now)
    wb_update = models.DateTimeField(default=timezone.now)
    multiplicity = models.IntegerField(blank=True, null=True)
    activity = models.BooleanField(default=True)
    comment = models.TextField(blank=True, null=True)
    media = models.ForeignKey(
        Media,
        on_delete=models.SET_NULL,
        null=True,
        db_column='media_id',
        related_name='products'
    )
    fitment = models.ForeignKey(
        Fitment,
        on_delete=models.SET_NULL,
        null=True,
        db_column='fitment_id',
        related_name='products'
    )
    type = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        db_column='type',
    )