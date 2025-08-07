from django.db import models

class AlembicVersion(models.Model):
    version_num = models.CharField(primary_key=True, max_length=32)

    class Meta:
        managed = False
        db_table = 'alembic_version'


class BrandAliases(models.Model):
    brand = models.ForeignKey('Brands', models.DO_NOTHING)
    marketplace = models.TextField()  # This field type is a guess.
    alias_name = models.CharField()

    class Meta:
        managed = False
        db_table = 'brand_aliases'
        unique_together = (('brand', 'marketplace', 'alias_name'),)


class Brands(models.Model):
    name = models.CharField(unique=True)
    description = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'brands'


class Categories(models.Model):
    name = models.CharField()
    ozon_category = models.ForeignKey('MarketplaceCategories', models.DO_NOTHING, blank=True, null=True)
    wb_category = models.ForeignKey('MarketplaceCategories', models.DO_NOTHING, related_name='categories_wb_category_set', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'categories'


class Characteristics(models.Model):
    weight = models.IntegerField()
    height = models.IntegerField()
    width = models.IntegerField()
    length = models.IntegerField()
    box_size = models.IntegerField()
    country = models.CharField()
    quantity_text = models.CharField()
    quantity_number = models.IntegerField()
    tn_ved = models.CharField()
    guarantee = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'characteristics'


class Fitment(models.Model):
    make = models.CharField()
    make_translit = models.CharField()
    model = models.CharField()
    model_translit = models.CharField()
    body = models.CharField()
    year_1 = models.IntegerField()
    year_2 = models.IntegerField()
    engine = models.CharField()
    power = models.IntegerField()
    engine_capacity = models.IntegerField()
    engine_code = models.CharField()

    class Meta:
        managed = False
        db_table = 'fitment'


class MarketplaceCategories(models.Model):
    marketplace = models.TextField()  # This field type is a guess.
    external_id = models.BigIntegerField()
    parent_external_id = models.BigIntegerField(blank=True, null=True)
    name = models.CharField()
    type_id = models.BigIntegerField(blank=True, null=True)
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'marketplace_categories'
        unique_together = (('marketplace', 'external_id'),)
    
    def __str__(self):
        return f"{self.marketplace} — {self.name}"


class Media(models.Model):
    image_1 = models.CharField()
    image_2 = models.CharField()
    image_3 = models.CharField()
    image_4 = models.CharField()
    image_5 = models.CharField()
    image_6 = models.CharField()
    image_7 = models.CharField()
    image_8 = models.CharField()
    image_9 = models.CharField()
    image_10 = models.CharField()
    rich = models.CharField()
    video = models.CharField()
    video_cover = models.CharField()
    pdf_instruction = models.CharField()
    certificate = models.CharField()

    class Meta:
        managed = False
        db_table = 'media'


class Oem(models.Model):
    oem_brand = models.CharField()
    oem_sku = models.CharField()
    cross_brand = models.CharField()
    cross_sku = models.CharField()

    class Meta:
        managed = False
        db_table = 'oem'


class OzonFitment(models.Model):
    ozon_sku = models.CharField()
    make = models.CharField()
    model = models.CharField()
    modification = models.CharField()

    class Meta:
        managed = False
        db_table = 'ozon_fitment'


class Prices(models.Model):
    purchase_price = models.IntegerField()
    price_ozon = models.IntegerField()
    profitability = models.IntegerField()
    profit = models.IntegerField()
    price = models.IntegerField()
    price_before_discount = models.IntegerField()
    vat = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'prices'


class Products(models.Model):
    brand = models.ForeignKey(Brands, models.DO_NOTHING)
    used_sku = models.CharField(blank=True, null=True)
    sku_1 = models.CharField(blank=True, null=True)
    sku_2 = models.CharField(blank=True, null=True)
    common_sku = models.CharField(blank=True, null=True)
    part_number = models.IntegerField(blank=True, null=True)
    ozon_sku = models.CharField(blank=True, null=True)
    ozon_id = models.IntegerField(blank=True, null=True)
    wb_id = models.IntegerField(blank=True, null=True)
    yandex_id = models.IntegerField(blank=True, null=True)
    id_1c = models.IntegerField(blank=True, null=True)
    id_mp = models.IntegerField(blank=True, null=True)
    name = models.CharField(blank=True, null=True)
    description = models.CharField(blank=True, null=True)
    keywords = models.CharField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    comment = models.CharField(blank=True, null=True)
    size = models.ForeignKey(Characteristics, models.DO_NOTHING, blank=True, null=True)
    price = models.ForeignKey(Prices, models.DO_NOTHING, blank=True, null=True)
    media = models.ForeignKey(Media, models.DO_NOTHING, blank=True, null=True)
    fitment = models.ForeignKey(Fitment, models.DO_NOTHING, blank=True, null=True)
    type = models.ForeignKey(Categories, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'products'
