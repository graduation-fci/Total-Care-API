from users.models import *
from medicines.serializers import CategoryGetSerializer, DrugSerializer, ImageSerializer, MedicineSerializer
from users.serializers import AddressSerializer
from .models import *
from re import S
from django.db import transaction
from pyparsing import null_debug_action
from rest_framework import serializers
from medicines.models import Medicine


class StoreMedicineSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    def get_images(self, obj):
        request = self.context.get('request')
        print(request)
        images = obj.images.all()
        if images:
            return [request.build_absolute_uri(image.image.url) for image in images]
        return []

    class Meta:
        model = Medicine
        fields = ['id', 'name', 'name_ar', 'price', 'images']
        depth = 1


class OrderItemSerializer(serializers.ModelSerializer):
    product = StoreMedicineSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'unit_price', 'quantity']



class OrderAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['street', 'city', 'description', 'phone','type','title']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    address = AddressSerializer()

    class Meta:
        model = Order
        fields = ['id', 'customer','address' ,'placed_at', 'order_status', 'payment_method' ,'items', 'total_price']



class UpdateOrderSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Order
        fields = ['order_status', 'address']

    def validate_order_status(self, value):
        user = self.context['request'].user
        order = self.instance

        # If user is staff, allow any update
        if user.is_staff:
            return value

        # If order status is confirmed, disallow any update
        if order.order_status == Order.ORDER_STATUS_CONFIRMED:
            raise serializers.ValidationError("Cannot update confirmed orders")

        # If order status is pending, allow cancellation
        if order.order_status == Order.ORDER_STATUS_PENDING:
            if value == Order.ORDER_STATUS_CANCELED:
                return value
            else:
                raise serializers.ValidationError("Invalid order status for non-staff user")

        # For other order statuses, disallow status update and address update
        if value != order.order_status:
            raise serializers.ValidationError("Cannot update order status for non-pending orders")
        if 'address' in self.initial_data:
            raise serializers.ValidationError("Cannot update address for non-pending orders")

        return value

    def validate_address(self, value):
        user = self.context['request'].user
        order = self.instance

        # If user is staff, allow any update
        if user.is_staff:
            return value

        # If order status is confirmed, disallow any update
        if order.order_status == Order.ORDER_STATUS_CONFIRMED:
            raise serializers.ValidationError("Cannot update confirmed orders")

        # If order status is pending, allow address update
        if order.order_status == Order.ORDER_STATUS_PENDING:
            return value

        # For other order statuses, disallow address update
        raise serializers.ValidationError("Cannot update address for non-pending orders")

            
    def update(self, instance, validated_data):
        address_data = validated_data.pop('address', None)
        if address_data:
            address = instance.address
            for key, value in address_data.items():
                setattr(address, key, value)
            address.save()

        return super().update(instance, validated_data)


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()
    address_id = serializers.IntegerField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError(
                'No cart with the given ID was found.')
        if CartItem.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError('The cart is empty.')
        return cart_id

    def validate_address_id(self, address_id):
        customer = Patient.objects.get(user_id=self.context['user_id'])
        if not Address.objects.filter(pk=address_id).exists():
            raise serializers.ValidationError(
                'No address with the given ID was found.')
        if not Address.objects.filter(customer=customer, id=address_id).exists():
            raise serializers.ValidationError('Not Allowed Address!!!')
        return address_id

    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            customer = Patient.objects.get(user_id=self.context['user_id'])
            address_id = self.validated_data['address_id']
            chosen_address = Address.objects.get(id=address_id)
            
            order_address = OrderAddress.objects.create(street= chosen_address.street,
                                                        city= chosen_address.city,
                                                        description= chosen_address.city,
                                                        phone=chosen_address.phone,
                                                        type = chosen_address.type,
                                                        title = chosen_address.title)

            cart_items = CartItem.objects.select_related(
                'product').filter(cart_id=cart_id)
            cart_total_price = sum(
                [item.quantity * item.product.price for item in cart_items])
            charge = 150
            order_total_price = cart_total_price + charge

            order = Order.objects.create(
                customer=customer, address=order_address, total_price=order_total_price)

            order_items = []
            for item in cart_items:
                product = item.product
                quantity = item.quantity
                if product.inventory - quantity >= 0:
                    order_items.append(OrderItem(
                        order=order,
                        product=product,
                        unit_price=item.product.price,
                        quantity=quantity
                    ))
                    product.inventory -= quantity
                    product.save()
                else:
                    raise serializers.ValidationError(
                        f'{product.name} inventory not suficient, only {product.inventory - 1} availabel')

            OrderItem.objects.bulk_create(order_items)
            cart_items.delete()
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
            raise serializers.ValidationError(
                'No product with the given ID was found.')
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




class WishListItemSerializer(serializers.ModelSerializer):
    product = StoreMedicineSerializer()

    class Meta:
        model = WishListItem
        fields = ['id', 'product']


class WishListSerializer(serializers.ModelSerializer):
    items = WishListItemSerializer(many=True, read_only=True)
    class Meta:
        model = WishList
        fields = ['id', 'items']


class AddWishListItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Medicine.objects.filter(pk=value).exists():
            raise serializers.ValidationError(
                'No product with the given ID was found.')
        return value

    def save(self, **kwargs):
        wishlist_id = self.context['wishlist_id']
        product_id = self.validated_data['product_id']
        

        try:
            wishlist_item = WishListItem.objects.get(
                wishlist_id=wishlist_id, product_id=product_id)
            
            self.instance = wishlist_item
        except WishListItem.DoesNotExist:
            self.instance = WishListItem.objects.create(
                wishlist_id=wishlist_id, **self.validated_data)

        return self.instance

    class Meta:
        model = WishListItem
        fields = ['id', 'product_id']


