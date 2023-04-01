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
import random
from itertools import chain
import json
from medicines.models import Medicine
from medicines.serializers import DrugSerializer, MedicineSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user: User):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['user_id'] = user.id
        token['profile_type'] = user.profile_type
        token['is_staff'] = user.is_staff
        # ...

        return token


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password',
                  'email', 'first_name', 'last_name', 'profile_type']


class UserSerializerDAB(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email',
                  'first_name', 'last_name', 'profile_type']


class SimpleMedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ['name', 'name_ar', 'drug']
        drug = DrugSerializer(many=True, read_only=True,
                              source='drug.medicines')
        depth = 1

class MedicationProfileGetSerializer(serializers.ModelSerializer):
    medicine = SimpleMedicineSerializer(many=True, read_only=True)
    class Meta:
        model = MedicationProfile
        fields = ['medicine']
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
        profile = MedicationProfile.objects.create(patient=patient, **validated_data)
        for medicine_id in medicines_data:
            try:
                medicine = Medicine.objects.get(id=medicine_id)
                profile.medicine.add(medicine)
            except Medicine.DoesNotExist:
                pass
        return profile

    class Meta:
        model = MedicationProfile
        fields = ['id', 'medicines']


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
