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
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

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


# class UserCreateSerializer(BaseUserCreateSerializer):
#     class Meta(BaseUserCreateSerializer.Meta):
#         fields = ['id', 'username', 'password',
#                   'email', 'first_name', 'last_name', 'profile_type']


User = get_user_model()

class UserCreateSerializer(BaseUserCreateSerializer):
    profile_type = serializers.ChoiceField(choices=User.TYPE_CHOICES, required=True, help_text=_('Required. Must be one of PAT, DR, CL, PHC.'), label=_('Profile Type'))
    
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'profile_type']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            profile_type=validated_data['profile_type']
        )
        return user


class UserSerializerDAB(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email',
                  'first_name', 'last_name', 'profile_type']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        social_accounts = instance.socialaccount_set.all()
        data['social_accounts'] = []
        for account in social_accounts:
            data['social_accounts'].append({
                'provider': account.provider,
                'uid': account.uid,
            })
        return data

