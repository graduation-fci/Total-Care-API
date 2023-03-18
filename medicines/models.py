from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


# Create your models here.

class Drug(models.Model):
    name = name = models.CharField(max_length=255, unique=True,verbose_name="drug name")

    def __str__(self) -> str:
        return self.name


class Medicine(models.Model):
    name = models.CharField(max_length=255, unique=True,verbose_name="medicine name")
    name_ar = models.CharField(max_length=255,unique=True, verbose_name="medicine name_ar")
    category = models.CharField(null=True,
                                max_length=255, verbose_name="medicine category")
    drug = models.ManyToManyField(Drug,related_name='drugs', null=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)])
    company = models.CharField(null=True, max_length=255, verbose_name="medicine company")
    parcode = models.BigIntegerField(null=True)
    def __str__(self) -> str:
        return self.title
