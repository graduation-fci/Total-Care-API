from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


# Create your models here.

class Drug(models.Model):
    name = name = models.CharField(max_length=255, unique=True,verbose_name="drug name")

    def __str__(self) -> str:
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="category name")
    name_ar = models.CharField(max_length=255)
    image = models.OneToOneField('Image', on_delete=models.CASCADE, related_name='category_image', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', 'name_ar']


class Medicine(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="medicine name")
    name_ar = models.CharField(max_length=255, unique=True, verbose_name="medicine name_ar")
    category = models.ManyToManyField(Category, related_name='medicines',blank=True)
    drug = models.ManyToManyField(Drug, related_name='medicines',blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    company = models.CharField(null=True, max_length=255, verbose_name="medicine company")
    parcode = models.BigIntegerField(null=True)

    def __str__(self):
        return self.name


class Image(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='medicine_images', null=True, blank=True)
    category = models.OneToOneField(Category, on_delete=models.CASCADE, related_name='category_image', null=True, blank=True)
    image = models.ImageField(upload_to='medicines/images')

    def __str__(self):
        return self.image.name


