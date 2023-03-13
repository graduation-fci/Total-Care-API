from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
  email = models.EmailField(unique=True)

  TYPE_PATIENT = 'PAT'
  TYPE_DOCTOR = 'DR'
  TYPE_CLINIC = 'CL'
  TYPE_PHARMACY = 'PHC'

  TYPE_CHOICES = [
        (TYPE_PATIENT, 'Student'),
        (TYPE_DOCTOR, 'Doctor'),
        (TYPE_CLINIC,'Clinic'),
        (TYPE_PHARMACY, 'Pharmacy')
    ]

  profile_type = models.CharField(
        max_length=3, choices=TYPE_CHOICES, null= True)
  

class Person(models.Model):
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta:
        ordering = ['user__first_name', 'user__last_name']