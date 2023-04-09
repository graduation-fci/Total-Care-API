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

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


#move later to seprated users app
class PatientViewSet(ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    #permission_classes = [IsAdminUser]


    @action(detail=False, methods=['GET', 'PUT', 'PATCH'], permission_classes=[IsAuthenticated])
    def me(self, request):
        Patient = self.queryset.get(
            user_id=request.user.id)
        if request.method == 'GET':
            serializer = PatientGetSerializer(Patient)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = PatientSerializer(Patient, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

# class MedicationProfileViewSet(ModelViewSet):
#     queryset = MedicationProfile.objects.all()
#     serializer_class = MedicationProfileSerializer

#     def get_serializer_context(self):
#         return {'user_id': self.request.user.id}

#     @action(detail=False, methods=['GET', 'PUT', 'PATCH','POST'], permission_classes=[IsAuthenticated])
#     def me(self, request):
#         patient = Patient.objects.get(user_id = self.request.user.id)
       
#         if request.method == 'GET':
#             try:
#                 profile =  self.queryset.get(
#                     patient_id=patient.id)
#             except:
#                 raise serializers.ValidationError("You don't have profiles yet")
            
#             serializer = MedicationProfileSerializer(profile)
#             return Response(serializer.data)
            
#         elif request.method == 'PUT':
#             try:
#                 profile =  self.queryset.get(
#                     patient_id=patient.id)
#             except:
#                 raise serializers.ValidationError("You don't have profiles yet")
#             serializer = MedicationProfileSerializer(profile, data=request.data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return Response(serializer.data)
#         elif request.method == 'POST':
#             serializer = MedicationProfileSerializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return Response(serializer.data)
    

class MedicationProfileViewSet(ModelViewSet):
    queryset = MedicationProfile.objects.all()
    serializer_class = MedicationProfileGetSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

    @action(detail=False, methods=['GET', 'PUT', 'PATCH','POST'], permission_classes=[IsAuthenticated])
    def me(self, request):
        patient = Patient.objects.get(user_id = self.request.user.id)
        serializer_context = self.get_serializer_context()  # <-- call get_serializer_context
       
        if request.method == 'GET':
            serializer = MedicationProfileGetSerializer
            try:
                profiles =  self.queryset.filter(patient_id = patient.id)
                print(profiles)
            except:
                raise serializers.ValidationError("You don't have profiles yet")
            
            serializer = MedicationProfileGetSerializer(profiles, context=serializer_context,many=True)  # <-- pass serializer_context
            return Response(serializer.data)
            
        elif request.method in ['PUT', 'PATCH']:
            serializer = MedicationProfileSerializer
            try:
                profile =  self.queryset.get(
                    patient_id=patient.id)
            except:
                raise serializers.ValidationError("You don't have profiles yet")
            serializer = MedicationProfileSerializer(profile, data=request.data, context=serializer_context)  # <-- pass serializer_context
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer= MedicationProfileSerializer
            serializer = MedicationProfileSerializer(data=request.data, context=serializer_context)  # <-- pass serializer_context
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

