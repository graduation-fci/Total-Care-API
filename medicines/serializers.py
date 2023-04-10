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
from django.core.exceptions import ValidationError
import os
import tempfile
from django.core.files.base import ContentFile
import base64
from io import BytesIO



class DrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = ['id','name']





from rest_framework import serializers
from .models import Image

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'medicine', 'category', 'image']

    def create(self, validated_data):
        image_path = validated_data.pop('image')
        instance = super().create(validated_data)
        with open(image_path, 'rb') as f:
            instance.image.save(image_path.split('/')[-1], f, save=True)
        return instance

    def update(self, instance, validated_data):
        image_path = validated_data.pop('image', None)
        instance = super().update(instance, validated_data)
        if image_path:
            with open(image_path, 'rb') as f:
                instance.image.save(image_path.split('/')[-1], f, save=True)
        return instance

class CategoryGetSerializer(serializers.ModelSerializer):
    image = ImageSerializer()
    class Meta:
        model = Category
        fields = ['id','name','name_ar', 'image']
        depth = 1

class CategorySerializer(serializers.ModelSerializer):
    image_file = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Category
        fields = ['id', 'name', 'name_ar', 'image_file']

    def create(self, validated_data):
        image_file = validated_data.pop('image_file', None)
        category = super().create(validated_data)
        if image_file:
            category.image = self._upload_image(image_file)
            category.save()
        return category

    def update(self, instance, validated_data):
        image_file = validated_data.pop('image_file', None)
        category = super().update(instance, validated_data)
        if image_file:
            category.image = self._upload_image(image_file)
            category.save()
        return category

    def _upload_image(self, image_file):
        try:
            with open(image_file, 'rb') as f:
                image_name = os.path.basename(image_file)
                image_content = f.read()
                return Image.objects.create(image=ContentFile(image_content, name=image_name))
        except FileNotFoundError:
            raise serializers.ValidationError('Image file not found')




#dont post single item outside bulk create
#response with drugs equal to null
class MedicineSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Medicine
        fields = ['id', 'name','name_ar','category','price','drug','company','parcode','medicine_images']
        drug = DrugSerializer(many=True,source='drug.medicines')
        medicine_images = ImageSerializer(many = True,source='image.medicine_images')
        depth = 1
        
class MedicineCreateSerializer(MedicineSerializer):
    def create(self, validated_data):
        image_files = validated_data.pop('image_files', None)
        med = super().create(validated_data)
        med_imgs = []
        if image_files:
            for image_file in image_files:
                _image = self._upload_image(image_file)
                med_imgs.append(_image)
            med.medicine_images = med_imgs
            med.save()
        return med

    def update(self, instance, validated_data):
        image_files = validated_data.pop('image_files', None)
        med = super().update(instance, validated_data)
        med_imgs = []
        if image_files:
            for image_file in image_files:
                _image = self._upload_image(image_file)
                med_imgs.append(_image)
            med.medicine_images = med_imgs
            med.save()

    def _upload_image(self, image_file):
        try:
            with open(image_file, 'rb') as f:
                image_name = os.path.basename(image_file)
                image_content = f.read()
                return Image.objects.create(image=ContentFile(image_content, name=image_name))
        except FileNotFoundError:
            raise serializers.ValidationError('Image file not found')