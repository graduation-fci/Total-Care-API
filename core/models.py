import os
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from medicines.models import Medicine
import phonenumbers
from django.core.exceptions import ValidationError

# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True)

    TYPE_PATIENT = 'PAT'
    TYPE_DOCTOR = 'DR'
    TYPE_CLINIC = 'CL'
    TYPE_PHARMACY = 'PHC'

    TYPE_CHOICES = [
        (TYPE_PATIENT, 'Patient'),
        (TYPE_DOCTOR, 'Doctor'),
        (TYPE_CLINIC, 'Clinic'),
        (TYPE_PHARMACY, 'Pharmacy')
    ]

    profile_type = models.CharField(
        max_length=3, choices=TYPE_CHOICES, null=True)



class Person(models.Model):
    
    TYPE_MALE = 'M'
    TYPE_FEMALE = 'F'

    GENDER_TYPE_CHOICES = [
        (TYPE_MALE, 'Male'),
        (TYPE_FEMALE, 'Female')
    ]
    
    def validate_phone_number(value):
        try:
            phone_number = phonenumbers.parse(value)
            if not phonenumbers.is_valid_number(phone_number):
                raise ValidationError("Invalid phone number")
        except phonenumbers.phonenumberutil.NumberParseException:
            raise ValidationError("Invalid phone number")

    phone = models.CharField(max_length=255, null=True, blank=True, validators=[validate_phone_number,])

    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices = GENDER_TYPE_CHOICES, null=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta:
        ordering = ['user__first_name', 'user__last_name']

class PersonImage(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, null=True, blank=True, related_name="image")
    image = models.ImageField(upload_to='users/images')

    def __str__(self):
        return self.image.name
    
    def delete(self, *args, **kwargs):
        # delete the image file from the file system
        os.remove(os.path.join(settings.MEDIA_ROOT, self.image.name))
        super().delete(*args, **kwargs)
        

class Patient(Person):
    # change later to selectedoptions
    TYPE_A_PLUS = 'A+'
    TYPE_A_MINUS = 'A-'
    TYPE_B_PLUS = 'B+'
    TYPE_B_MINUS = 'B-'
    TYPE_AB_PLUS = 'AB+'
    TYPE_AB_MINUS = 'AB-'
    TYPE_O_PLUS = 'O+'
    TYPE_O_MINUS = 'O-'

    BLOOD_TYPE_CHOICES = [
        (TYPE_A_PLUS, 'A+'),
        (TYPE_A_MINUS, 'A-'),
        (TYPE_B_PLUS, 'B+'),
        (TYPE_B_MINUS, 'B-'),
        (TYPE_AB_PLUS, 'AB+'),
        (TYPE_AB_MINUS, 'AB-'),
        (TYPE_O_PLUS, 'O+'),
        (TYPE_O_MINUS, 'O-')
    ]
    bloodType = models.CharField(max_length=3, choices = BLOOD_TYPE_CHOICES, null=True)





class Doctor(Person):
    #change later to selectedoptions
    specialization = models.CharField(max_length=255)
