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
from .models import Exam, RightAnswer, Student, Subject, Department, Level
from .serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import *

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class PatientViewSet(ModelViewSet):
    queryset = Patient.objects.prefetch_related('medications').all()
    serializer_class = PatientSerializer
    permission_classes = [IsAdminUser]


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
