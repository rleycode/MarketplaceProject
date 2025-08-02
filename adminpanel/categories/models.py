from django.db import models

class MarketplaceEnum(models.TextChoices):
    OZON = "OZON"
    WB = "WB"
    YANDEX = "YANDEX"

class MarketplaceCategory(models.Model):
    marketplace = models.CharField(max_length=20, choices=MarketplaceEnum.choices)
    external_id = models.BigIntegerField()
    parent_external_id = models.BigIntegerField(null=True, blank=True)
    name = models.CharField(max_length=255)
    full_path = models.CharField(max_length=255, null=True, blank=True)
    type_id = models.BigIntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("marketplace", "external_id")
        db_table = "marketplace_categories"

    def __str__(self):
        return f"{self.marketplace}: {self.name}"

class Category(models.Model):
    name = models.CharField(max_length=255)
    ozon_category = models.ForeignKey(
        MarketplaceCategory, null=True, blank=True, related_name="ozon_categories", on_delete=models.SET_NULL
    )
    wb_category = models.ForeignKey(
        MarketplaceCategory, null=True, blank=True, related_name="wb_categories", on_delete=models.SET_NULL
    )

    class Meta:
        db_table = "categories"

    def __str__(self):
        return self.name