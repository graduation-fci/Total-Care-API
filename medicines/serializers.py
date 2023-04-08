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


class DrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = ['id','name']

#dont post single item outside bulk create
#response with drugs equal to null
class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ['id', 'name','name_ar','category','price','drug','company','parcode']
        drug = DrugSerializer(many=True,source='drug.medicines')
        depth = 1
        
