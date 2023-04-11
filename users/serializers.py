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
    medicine_images = ImageSerializer(many = True)
    class Meta:
        model = Medicine
        fields = ['id','name', 'name_ar', 'drug','medicine_images']
        drug = DrugSerializer(many=True, read_only=True,
                              source='drug.medicines')
        depth = 1


class MedicationProfileGetSerializer(serializers.ModelSerializer):
    medicine = SimpleMedicineSerializer(many=True, read_only=True)

    class Meta:
        model = MedicationProfile
        fields = ['id','medicine']
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
        instance.medicine.set(validated_data.get('medicines', []))
        instance.save()
        return instance
    
    class Meta:
        model = MedicationProfile
        fields = ['id', 'medicines']
        depth = 1



class PatientSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    profiles = MedicationProfileSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = ['id', 'user_id', 'phone',
                  'birth_date', 'profiles', 'bloodType']
        # MedicationProfile = MedicationProfileSerializer(many=True, read_only=True, source='drug.medicines')
        depth = 1


class PatientGetSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    profiles = MedicationProfileSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = ['id', 'user_id', 'phone', 'birth_date', 'profiles']
        depth = 1
