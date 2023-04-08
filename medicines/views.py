
from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action, permission_classes, api_view
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny, \
    DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet , ViewSet
from rest_framework import status
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from medicines.filters import MedicineFilter
from .serializers import *
from medicines.pagination import DefaultPagination
from django.shortcuts import render
from medicines.graph_grpc import graph_pb2, graph_pb2_grpc
import grpc
from django.http import HttpResponse, JsonResponse
import json
from google.protobuf.json_format import MessageToDict



class MedicineViewSet(ModelViewSet):
    queryset = Medicine.objects.prefetch_related('drug').all()
    serializer_class = MedicineSerializer
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_class = MedicineFilter
    search_fields = ['name']
    ordering_fields = ['name', 'price']

    @action(detail=False, methods=['POST'])
    def bulk_create(self, request):
        drug_names = request.data[0].pop('drug', []) if request.data else []  # Remove drug names from request data
        drugs = []
        for drug_name in drug_names:
            try:
                drug = Drug.objects.get(name=drug_name)
            except Drug.DoesNotExist:
                drug = Drug.objects.create(name=drug_name)
            drugs.append(drug)
        serializer = MedicineSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        medicines = serializer.save(drug=drugs)  # Pass the list of Drug objects to the serializer
        return Response(MedicineSerializer(medicines, many=True).data)


class DrugViewSet(ModelViewSet):
    queryset = Drug.objects.all()
    serializer_class = DrugSerializer
    pagination_class = DefaultPagination

    @action(detail=False, methods=['POST'])
    def bulk_create(self, request):
        serializer = DrugSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        drugs = serializer.save()
        return Response(DrugSerializer(drugs, many=True).data)
    
channel = grpc.insecure_channel('localhost:50051')

class InteractionsViewSet(ViewSet):
    def create(self, request):
        data = request.data
        medicines = data.get('medicine', [])
        
        #transformed_medicines = Operation.transform(medicines)

        my_request = graph_pb2.CheckInteractionsRequest()
        for medicine in medicines:
            name_en = medicine.get('name', '')
            name_ar = medicine.get('name_ar', '')
            drugs = [drug.get('name', '') for drug in medicine.get('drug', [])]

            
            my_med = graph_pb2.Medecine(name=graph_pb2.I18n(name_en=name_en,name_ar=name_ar), drugs=drugs)
            
            my_request.medecines.extend([my_med])

        stub = graph_pb2_grpc.GraphServiceStub(channel)

    
        response = stub.CheckInteractions(my_request)
        
        response_dict = MessageToDict(response)
        return Response(response_dict, status=status.HTTP_200_OK)

