from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet , ViewSet
from rest_framework import status
from medicines.filters import MedicineFilter
from .serializers import *
from medicines.pagination import DefaultPagination
from medicines.graph_grpc import graph_pb2, graph_pb2_grpc
import grpc
from rest_framework.exceptions import ValidationError
from django.db.models.deletion import ProtectedError
from google.protobuf.json_format import MessageToDict
from users.serializers import SimpleMedicineSerializer
from .models import Image



class SimpleMedicineViewSet(ModelViewSet):
    queryset = Medicine.objects.prefetch_related('drug').all()
    pagination_class = DefaultPagination
    serializer_class = SimpleMedicineSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = MedicineFilter
    search_fields = ['name']
    ordering_fields = ['name', 'price']


class MedicineViewSet(ModelViewSet):
    
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = MedicineFilter
    search_fields = ['name']
    ordering_fields = ['name', 'price']

    def get_serializer_class(self):

        if self.request.method == 'PATCH' and 'products' in self.request.path:
            return MedicinePatchSerializer
        elif self.request.method == 'POST' or self.request.method == 'PATCH' :
            return MedicineCreateSerializer
        return MedicineSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Medicine.objects.prefetch_related('drug').all()
        
        return Medicine.objects.prefetch_related('drug').filter(is_active = True)
    
    def perform_destroy(self, instance):
        try:
            instance.delete()
        except:
            raise serializers.ValidationError("Cannot delete protected object... you can deactivate it by changing the is_active")
    
    @action(detail=False, methods=['POST'])
    def bulk_create(self, request):
        

        success_list = []
        fail_list = []

        for data in request.data:
            try:
                drug_names = data.pop('drug', []) if request.data else []  # Remove drug names from request data
                drugs = []
                for drug_name in drug_names:
                    try:
                        drug = Drug.objects.get(name=drug_name)
                    except Drug.DoesNotExist:
                        drug = Drug.objects.create(name=drug_name)
                    drugs.append(drug)
                
                category_names = data.pop('category', []) if request.data else []  # Remove category names from request data
                categories = []
                
                if len(category_names) > 0:
                    for category_name in category_names:
                        print(category_name)
                        print(data['name'])
                        category = Category.objects.get(name=category_name)
                        categories.append(category)
                
                

                serializer = MedicineCreateSerializer(data=data)
                
                serializer.is_valid(raise_exception=True)
                
                medicine = serializer.save(drug=drugs,category=categories)
                
                success_list.append(medicine)
            except ValidationError as e:
                fail_list.append((data, str(e)))

        response_data = {
            'success': MedicineSerializer(success_list, many=True).data,
            'fail': fail_list,
            'success_count': len(success_list),
            'fail_count': len(fail_list),
        }
        return Response(response_data)
    
    @action(detail=False, methods=['PATCH'])
    def bulk_patch(self, request):
        success_list = []
        fail_list = []
        for data in request.data:
            medicine = Medicine.objects.filter(id=data.pop('id')).first()
            if not medicine:
                fail_list.append({'name': data['name'], 'error': 'Medicine does not exist'})
                continue  # Skip if the medicine does not exist

            drug_names = data.pop('drug', []) if request.data else []  # Remove drug names from request data
            drugs = []
            for drug_name in drug_names:
                try:
                    drug = Drug.objects.get(name=drug_name)
                except Drug.DoesNotExist:
                    drug = Drug.objects.create(name=drug_name)
                drugs.append(drug)
            
            category_names = data.pop('category', []) if request.data else []  # Remove category names from request data
            categories = []
            
            for category_name in category_names:
                category = Category.objects.get(name=category_name)
                categories.append(category)
            print(category_names)

            serializer = self.get_serializer(medicine, data=data, partial=True)
            try:
                serializer.is_valid(raise_exception=True)
                success_list.append(serializer.save(drug=drugs,category=categories))
            except serializers.ValidationError as e:
                fail_list.append({'name': data['name'], 'error': str(e)})
        return Response({
            'updated': len(success_list),
            'failed': len(fail_list),
            'fail_list': fail_list,
        })

    @action(detail=False, methods=['DELETE'])
    def bulk_delete(self, request):
        medicine_ids = request.data.get('ids', [])  # Get the list of medicine ids to delete
        deleted_medicines = []
        failed_medicines = []
        protected_ids = []
        for medicine_id in medicine_ids:
            try:
                medicine = Medicine.objects.get(id=medicine_id)
                medicine.delete()
                deleted_medicines.append(medicine_id)
            except Medicine.DoesNotExist:
                failed_medicines.append({'id': medicine_id, 'error': 'Medicine not found'})
            except ProtectedError:
                failed_medicines.append({'id': medicine_id, 'error': 'Medicine is related to other models'})
                protected_ids.append(medicine_id)
        response_data = {'deleted': deleted_medicines,'deleted_count' : len(deleted_medicines),'protected_ids':protected_ids, 'failed': failed_medicines,'failed_count': len(failed_medicines) }
        return Response(response_data)
    
    @action(detail=False, methods=['post'], url_path='bulk_deactivate')
    def bulk_deactivate(self, request):
        medicine_ids = request.data.get('ids', [])
        if not medicine_ids:
            return Response({'message': 'No medicine ids provided'})

        medicines_to_deactivate = Medicine.objects.filter(id__in=medicine_ids)
        medicines_to_deactivate.update(is_active=False)
        return Response({'message': f'{medicines_to_deactivate.count()} medicines have been deactivated'})
    
    @action(detail=False, methods=['post'], url_path='bulk_activate')
    def bulk_activate(self, request):
        medicine_ids = request.data.get('ids', [])
        if not medicine_ids:
            return Response({'message': 'No medicine ids provided'})

        medicines_to_activate = Medicine.objects.filter(id__in=medicine_ids)
        medicines_to_activate.update(is_active=True)
        return Response({'message': f'{medicines_to_activate.count()} medicines have been activated'})


class DrugViewSet(ModelViewSet):
    queryset = Drug.objects.all()
    serializer_class = DrugSerializer
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    @action(detail=False, methods=['POST'])
    def bulk_create(self, request):
        success_list = []
        fail_list = []

        for data in request.data:
            try:
                serializer = DrugSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                drug = serializer.save()
                success_list.append(drug)
            except ValidationError as e:
                fail_list.append((data, str(e)))

        response_data = {
            'success': DrugSerializer(success_list, many=True).data,
            'fail': fail_list,
            'success_count': len(success_list),
            'fail_count': len(fail_list),
        }
        return Response(response_data)
    
    @action(detail=False, methods=['PATCH'])
    def bulk_patch(self, request):
        success_list = []
        fail_list = []
        for data in request.data:
            drug = Drug.objects.filter(id=data.pop('id')).first()
            if not drug:
                fail_list.append({'name': data['name'], 'error': 'Drug does not exist'})
                continue  # Skip if the drug does not exist
            serializer = self.get_serializer(drug, data=data, partial=True)
            try:
                serializer.is_valid(raise_exception=True)
                success_list.append(serializer.save())
            except serializers.ValidationError as e:
                fail_list.append({'name': data['name'], 'error': str(e)})
        return Response({
            'updated': len(success_list),
            'failed': len(fail_list),
            'fail_list': fail_list,
        })

    @action(detail=False, methods=['DELETE'])
    def bulk_delete(self, request):
        ids = request.data.get('ids', [])
        drugs = self.get_queryset().filter(id__in=ids)
        deleted_count, _ = drugs.delete()
        return Response({'deleted': deleted_count})

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'name_ar']
    ordering_fields = ['name', 'name_ar']
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CategoryGetSerializer
        return CategorySerializer

    @action(detail=False, methods=['POST'])
    def bulk_create(self, request):
        success_list = []
        fail_list = []

        for data in request.data:
            try:
                serializer = CategorySerializer(data=data)
                serializer.is_valid(raise_exception=True)
                category = serializer.save()
                success_list.append(category)
            except ValidationError as e:
                fail_list.append((data, str(e)))

        response_data = {
            'success': CategorySerializer(success_list, many=True).data,
            'fail': fail_list,
            'success_count': len(success_list),
            'fail_count': len(fail_list),
        }
        return Response(response_data)

    @action(detail=False, methods=['PATCH'])
    def bulk_patch(self, request):
        success_list = []
        fail_list = []
        for data in request.data:
            category = Category.objects.filter(id=data.pop('id')).first()
            if not category:
                fail_list.append({'name': data['name'], 'error': 'Category does not exist'})
                continue  # Skip if the category does not exist
            serializer = self.get_serializer(category, data=data, partial=True)
            try:
                serializer.is_valid(raise_exception=True)
                success_list.append(serializer.save())
            except serializers.ValidationError as e:
                fail_list.append({'name': data['name'], 'error': str(e)})
        return Response({
            'updated': len(success_list),
            'failed': len(fail_list),
            'fail_list': fail_list,
        })

    @action(detail=False, methods=['DELETE'])
    def bulk_delete(self, request):
        ids = request.data.get('ids', [])
        categories = self.get_queryset().filter(id__in=ids)
        deleted_count, _ = categories.delete()
        return Response({'deleted': deleted_count})




    


class InteractionsViewSet(ViewSet):
    def create(self, request):
        data = request.data
        medicines = data.get('medicine', [])
        
        #transformed_medicines = Operation.transform(medicines)

        channel = grpc.insecure_channel('localhost:50051')

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
        
        # print("id" , data['id'])
        # if data['id'] != None:
        #     user_id =self.request.user.id
        #     patient = Patient.objects.get(user_id=user_id)
        #     profile_ids = MedicationProfile.objects.filter(patient=patient).values_list('id', flat=True)

        #     if data['id'] in profile_ids:
        #         print("True")


        return Response(response_dict, status=status.HTTP_200_OK)



class ImageViewSet(ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = UploadImageSerializer
    pagination_class = DefaultPagination

    @action(detail=False, methods=['POST'])
    def bulk_create_images(self, request):
        images = request.FILES.getlist('images')
        success_ids = []
        failed_items = []

        for image in images:
            serializer = self.get_serializer(data={'image': image})
            if serializer.is_valid():
                serializer.save()
                success_ids.append(serializer.data['id'])
            else:
                failed_items.append({'item': image.name, 'cause': serializer.errors})
        
        response_data = {
            'success_count': len(success_ids),
            'success_ids': success_ids,
            'fail_count': len(failed_items),
            'failed_items': failed_items
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['DELETE'])
    def bulk_delete_images(self, request):
        image_ids = request.data.get('ids', [])
        success_ids = []
        failed_items = []

        for image_id in image_ids:
            try:
                image = Image.objects.get(id=image_id)
                image.delete()
                success_ids.append(image_id)
            except Image.DoesNotExist:
                failed_items.append({'item': image_id, 'cause': 'Image not found'})
        
        response_data = {
            'deleted_count': len(success_ids),
            'deleted_ids': success_ids,
            'fail_count': len(failed_items),
            'failed_items': failed_items
        }
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)
