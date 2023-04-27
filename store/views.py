from django.shortcuts import render
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

from store.filters import OrderFilter


from .serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import *
from core.models import *
from rest_framework.viewsets import GenericViewSet
# Create your views here.
# Create your views here.
    
class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = OrderFilter
    
    ordering_fields = ['placed_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        context['user_id']= self.request.user.id
        return context
    
    def get_permissions(self):
        if self.request.method in ['DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order, context=self.get_serializer_context())
        return Response(serializer.data)
    
    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Order.objects.prefetch_related('address').all()

        customer_id = Patient.objects.only('id').get(user_id=user.id)
        return Order.objects.prefetch_related('address').filter(customer_id=customer_id)

class CartViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch']
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Cart.objects.all()

        customer_id = Patient.objects.only('id').get(user_id=user.id)
        return Cart.objects.filter(customer_id=customer_id)


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        context['user_id'] = self.request.user.id
        context['cart_id'] = self.kwargs['cart_pk']
        return context
    
    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')