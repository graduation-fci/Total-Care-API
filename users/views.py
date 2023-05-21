from medicines.permissions import FullDjangoModelPermissions, IsAdminOrReadOnly
from medicines.pagination import DefaultPagination
from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action, permission_classes, api_view
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny, \
    DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from .filters import *
from .serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import *
from core.models import *

# Create your views here.

class AddressViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = AddressSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Address.objects.all()
        patient_id = Patient.objects.only('id').get(user_id=user.id)
        return Address.objects.filter(customer_id = patient_id)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        context['user_id']= self.request.user.id
        return context
    

class PatientViewSet(ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAdminUser]

    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     context['request'] = self.request
    #     context['user_id']= self.request.user.id
    #     return context

    @action(detail=False, methods=['GET', 'PUT', 'PATCH'], permission_classes=[IsAuthenticated])
    def me(self, request):
        Patient = self.queryset.get(
            user_id=request.user.id)
        if request.method == 'GET':
            serializer = PatientGetSerializer(Patient, context={'request': request},)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = PatientSerializer(Patient, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = PatientSerializer(Patient, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

class MedicationProfileViewSet(ModelViewSet):
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['title']
    

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MedicationProfileGetSerializer
        return MedicationProfileSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        context['user_id']= self.request.user.id
        return context

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return MedicationProfile.objects.prefetch_related('medicine').all().order_by('title')
        
        patient_id = Patient.objects.only('id').get(user_id=user.id)

        return MedicationProfile.objects.prefetch_related('medicine').filter(patient_id = patient_id).order_by('title')
    
    
class ImageViewSet(ModelViewSet):
    
    serializer_class = UploadImageSerializer
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return PersonImage.objects.all()

        person = Person.objects.get(user_id=user.id)
        return PersonImage.objects.filter(person = person)
