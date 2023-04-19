from django.db import models
from core.models import Patient
from medicines.models import Medicine



# Create your models here.

class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='adresses')
    description = models.TextField(null=True, blank=True)
    
class MedicationProfile (models.Model):
    title = models.CharField(max_length=255)
    medicine = models.ManyToManyField(Medicine, related_name='medicines')
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name='profiles')