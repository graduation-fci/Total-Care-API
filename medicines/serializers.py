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
import io
import requests
from django.core.files.images import ImageFile


class DrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = ['id','name']







class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id','image']
    
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
    

class UploadImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id','image']
    
    # def handle_uploaded_file(self, file):
    #     with open(os.path.join(settings.MEDIA_ROOT, file.name), 'wb+') as destination:
    #         for chunk in file.chunks():
    #             destination.write(chunk)
    #     return file.name

    # def create(self, validated_data):
    #     image = validated_data.get('image')
    #     image_path = self.handle_uploaded_file(image)
    #     image_obj = Image.objects.create(image=image_path)
    #     return image_obj

class GeneralCategoryGetSerializer(serializers.ModelSerializer):
    image = ImageSerializer()
    class Meta:
        model = GeneralCategory
        fields = ['id','name','name_ar', 'image']
        depth = 1
class CategoryGetSerializer(serializers.ModelSerializer):
    image = ImageSerializer()
    general_category = GeneralCategoryGetSerializer()
    class Meta:
        model = Category
        fields = ['id','name','name_ar', 'image', 'general_category']
        depth = 1



class CategorySerializer(serializers.ModelSerializer):
    image_file = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Category
        fields = ['id', 'name', 'name_ar', 'image_file', 'general_category']

    def create(self, validated_data):
        print("entered")
        image_file = validated_data.pop('image_file', None)
        print(image_file)
        category = super().create(validated_data)
        if image_file:
            new_image = self._upload_image(image_file)
            new_image.category = category
            new_image.save()
        return category

    def update(self, instance, validated_data):
        image_file = validated_data.pop('image_file', None)
        category = super().update(instance, validated_data)
        if image_file:
            new_image = self._upload_image(image_file)
            new_image.category = category
            new_image.save()
        return category

    def _upload_image(self, image_file):
        if str(image_file).isdigit():
            # Image file is an ID
            image = Image.objects.get(id=image_file)
            return image
        elif image_file.startswith('http'):
            # Image file is a URL
            response = requests.get(image_file)
            response.raise_for_status()
            image_content = response.content
            image_name = os.path.basename(image_file)
            in_memory_file = io.BytesIO(image_content)
            return Image.objects.create(image=ImageFile(in_memory_file, name=image_name))
        else:
            # Image file is a file path
            try:
                with open(image_file, 'rb') as f:
                    image_name = os.path.basename(image_file)
                    image_content = f.read()
                    return Image.objects.create(image=ContentFile(image_content, name=image_name))
            except FileNotFoundError:
                raise serializers.ValidationError('Image file not found')

class GeneralCategorySerializer(serializers.ModelSerializer):
    image_file = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = GeneralCategory
        fields = ['id', 'name', 'name_ar', 'image_file']
    
    def create(self, validated_data):
        print("entered")
        image_file = validated_data.pop('image_file', None)
        print(image_file)
        general_category = super().create(validated_data)
        if image_file:
            new_image = self._upload_image(image_file)
            new_image.general_category = general_category
            new_image.save()
        return general_category

    def update(self, instance, validated_data):
        image_file = validated_data.pop('image_file', None)
        general_category = super().update(instance, validated_data)
        if image_file:
            new_image = self._upload_image(image_file)
            new_image.general_category = general_category
            new_image.save()
        return general_category

    def _upload_image(self, image_file):
        if str(image_file).isdigit():
            # Image file is an ID
            image = Image.objects.get(id=image_file)
            return image
        elif image_file.startswith('http'):
            # Image file is a URL
            response = requests.get(image_file)
            response.raise_for_status()
            image_content = response.content
            image_name = os.path.basename(image_file)
            in_memory_file = io.BytesIO(image_content)
            return Image.objects.create(image=ImageFile(in_memory_file, name=image_name))
        else:
            # Image file is a file path
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
    medicine_images = ImageSerializer(many = True)
    category = CategoryGetSerializer(many = True)
    in_stock = serializers.BooleanField(read_only=True)
    class Meta:
        model = Medicine
        fields = ['id', 'name','name_ar','category','price','is_active','in_stock','drug','company','parcode','medicine_images']
        drug = DrugSerializer(many=True,source='drug.medicines')
        depth = 1
    
    
            


#created for updating or removing specific images from medicine
class MedicinePatchSerializer(serializers.ModelSerializer):
    medicine_images = serializers.PrimaryKeyRelatedField(
        queryset=Image.objects.all(),
        many=True,
        required=False
    )
    category = CategoryGetSerializer(many = True)
    class Meta:
        model = Medicine
        fields = ['id', 'name','name_ar','category','inventory','is_active','price','drug','company','parcode','medicine_images']
        drug = DrugSerializer(many=True,source='drug.medicines')
        depth = 1


class MedicineCreateSerializer(serializers.ModelSerializer):
    image_files = serializers.ListField(child = serializers.CharField(),write_only=True, required=False)

    class Meta:
        model = Medicine
        fields = ['id', 'name','name_ar','category','is_active','price','drug','company','inventory','parcode','image_files']
        drug = DrugSerializer(many=True,source='drug.medicines')

    def create(self, validated_data):
        print("entered")
        image_files = validated_data.pop('image_files', None)
        print(image_files)
        print("heyyyyyyy")
        med = super().create(validated_data)
        if image_files:
            self.create_images(med, image_files)
        return med

    def update(self, instance, validated_data):
        image_files = validated_data.pop('image_files', None)
        
        med = super().update(instance, validated_data)
        if image_files:
            self.create_images(med, image_files)
        return med

    def create_images(self, med, image_files):
        print("Creating images...")
        med_imgs = []
        if str(image_files[0]).isdigit():
        # Image file is a list of ids
            for image_id in image_files:
                try:
                    image = Image.objects.get(id=image_id)
                    med_imgs.append(image)
                except Image.DoesNotExist:
                    pass
        else:
            for image_file in image_files:
                _image = self._upload_image(image_file)
                med_imgs.append(_image)
        print(med_imgs)      
        if str(image_files[0]).isdigit():
            for img in med_imgs:
                img.medicine = med
                img.save()
        else:
            for img in med_imgs:
                Image.objects.create(medicine=med, image=img)
    
    def _upload_image(self, image_file):
        if image_file.startswith('http'):
            # Image file is a URL
            response = requests.get(image_file)
            response.raise_for_status()
            image_content = response.content
            image_name = os.path.basename(image_file)
        else:
            # Image file is a file path
            try:
                with open(image_file, 'rb') as f:
                    image_name = os.path.basename(image_file)
                    image_content = f.read()
            except FileNotFoundError as e:
                raise serializers.ValidationError(f'Image file not found: {image_file}. Error: {e}')

        return ContentFile(image_content, name=image_name)


