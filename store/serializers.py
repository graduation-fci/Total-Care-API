from users.models import *
from medicines.serializers import CategoryGetSerializer, DrugSerializer, ImageSerializer, MedicineSerializer
from .models import *
from re import S
from django.db import transaction
from pyparsing import null_debug_action
from rest_framework import serializers
from medicines.models import Medicine




class StoreMedicineSerializer(serializers.ModelSerializer):
    medicine_images = serializers.SerializerMethodField()

    def get_medicine_images(self, obj):
        request = self.context.get('request')
        print(request)
        images = obj.medicine_images.all()
        if images:
            return [request.build_absolute_uri(image.image.url) for image in images]
        return []

    
    class Meta:
        model = Medicine
        fields = ['id', 'name','name_ar','price','medicine_images']
        depth = 1

class OrderItemSerializer(serializers.ModelSerializer):
    product = StoreMedicineSerializer()
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'unit_price', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'placed_at', 'payment_status', 'items', 'total_price']


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()
    address_id = serializers.IntegerField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError('No cart with the given ID was found.')
        if CartItem.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError('The cart is empty.')
        return cart_id
    
    def validate_address_id(self, address_id):
        customer = Patient.objects.get(user_id=self.context['user_id'])
        if not Address.objects.filter(pk=address_id).exists():
            raise serializers.ValidationError('No address with the given ID was found.')
        if not Address.objects.filter(customer=customer, id=address_id).exists():
            raise serializers.ValidationError('Not Allowed Address!!!')
        return address_id
    
    
    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            customer = Patient.objects.get(user_id=self.context['user_id'])
            address_id = self.validated_data['address_id']
            order_address = Address.objects.get(id=address_id)
            
            cart_items = CartItem.objects.select_related('product').filter(cart_id=cart_id)
            cart_total_price = sum([item.quantity * item.product.price for item in cart_items])
            charge = 150
            order_total_price = cart_total_price + charge
            
            order = Order.objects.create(customer=customer, address=order_address, total_price=order_total_price)

            order_items = [
                OrderItem(
                    order=order,
                    product=item.product,
                    unit_price=item.product.price,
                    quantity=item.quantity
                ) for item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)
            # CartItem.objects.delete(cart_items)            
            return order


class CartItemSerializer(serializers.ModelSerializer):
    product = StoreMedicineSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.price

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart):
        return sum([item.quantity * item.product.price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Medicine.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No product with the given ID was found.')
        return value

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(
                cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data)

        return self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']
    

