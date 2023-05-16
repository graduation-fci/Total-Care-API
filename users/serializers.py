import os
from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from re import S
from django.db import transaction
from django.db.models import Prefetch
from pyparsing import null_debug_action
from rest_framework import serializers
from django.utils import timezone
from .models import *
from core.models import *
import random
from itertools import chain
import json
from medicines.models import Medicine
from medicines.serializers import DrugSerializer, ImageSerializer



class SimpleMedicineSerializer(serializers.ModelSerializer):
    medicine_images = serializers.SerializerMethodField()

    def get_medicine_images(self, obj):
        request = self.context.get('request')
        images = obj.medicine_images.all()
        if images:
            return [request.build_absolute_uri(image.image.url) for image in images]
        return []
    class Meta:
        model = Medicine
        fields = ['id','name', 'name_ar', 'drug','medicine_images']
        drug = DrugSerializer(many=True, read_only=True,
                              source='drug.medicines')
        depth = 1

class UploadImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonImage
        fields = ['id','image']
    
    def handle_uploaded_file(self, file):
        with open(os.path.join(settings.MEDIA_ROOT, file.name), 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        return file.name

    def create(self, validated_data):
        image = validated_data.get('image')
        image_path = self.handle_uploaded_file(image)
        image_obj = PersonImage.objects.create(image=image_path)
        return image_obj

class MedicationProfileGetSerializer(serializers.ModelSerializer):
    medicine = SimpleMedicineSerializer(many=True, read_only=True)

    class Meta:
        model = MedicationProfile
        fields = ['id','title','medicine']
        depth = 1


class MedicationProfileSerializer(serializers.ModelSerializer):

    medicines = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True
    )

    def create(self, validated_data):
        user_id = self.context['user_id']
        patient = Patient.objects.get(user_id=user_id)
        medicines_data = validated_data.pop('medicines', [])
        profile = MedicationProfile.objects.create(
            patient=patient, **validated_data)
        for medicine_id in medicines_data:
            try:
                medicine = Medicine.objects.get(id=medicine_id)
                profile.medicine.add(medicine)
            except Medicine.DoesNotExist:
                pass
        return profile
    
    def update(self, instance, validated_data):
        # Update the fields on the instance object
        if 'title' in validated_data:
            instance.title = validated_data.get('title', instance.title)
        if 'medicines' in validated_data:
            instance.medicine.set(validated_data['medicines'])
        instance.save()
        return instance
    
    class Meta:
        model = MedicationProfile
        fields = ['id', 'title','medicines']
        depth = 1

class AddressSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user_id = self.context['user_id']
        patient = Patient.objects.only('id').get(user_id=user_id)
        return Address.objects.create(customer_id=patient.id, **validated_data)

    class Meta:
        model = Address
        fields = ['id', 'street', 'city', 'description', 'phone','type','title']

class PatientSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    profiles = MedicationProfileSerializer(many=True, read_only=True)
    # adresses = AddressSerializer(many=True)

    class Meta:
        model = Patient
        fields = ['id', 'user_id', 'phone', 'birth_date', 'profiles', 'bloodType', 'image']
        # MedicationProfile = MedicationProfileSerializer(many=True, read_only=True, source='drug.medicines')
        depth = 1


class PatientGetSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    profiles = MedicationProfileSerializer(many=True, read_only=True)
    image = ImageSerializer(read_only=True)

    class Meta:
        model = Patient
        fields = ['id', 'user_id', 'phone', 'birth_date', 'profiles', 'image']
        depth = 1
