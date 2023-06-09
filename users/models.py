from django.db import models
from core.filters import User
from core.models import Patient
from medicines.models import Medicine
import phonenumbers
from django.core.exceptions import ValidationError


# Create your models here.

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

class Address(models.Model):
    
    ADD_TYPE_HOME = 'Home'
    ADD_TYPE_BUISNESS = 'Business'
    
    ADD_TYPE_CHOICESS = [
        (ADD_TYPE_HOME, 'Home'),
        (ADD_TYPE_BUISNESS, 'Business')
    ]
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=8, choices=ADD_TYPE_CHOICESS, default=ADD_TYPE_HOME)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='adresses')
    description = models.TextField(null=True, blank=True)
    
    def validate_phone_number(value):
        try:
            phone_number = phonenumbers.parse(value)
            if not phonenumbers.is_valid_number(phone_number):
                raise ValidationError("Invalid phone number")
        except phonenumbers.phonenumberutil.NumberParseException:
            raise ValidationError("Invalid phone number")

    phone = models.CharField(max_length=255, validators=[validate_phone_number])
    
class MedicationProfile (models.Model):
    title = models.CharField(max_length=255)
    medicine = models.ManyToManyField(Medicine, related_name='medicines')
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name='profiles')