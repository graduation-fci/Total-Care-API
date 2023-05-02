from uuid import uuid4
from django.db import models
from core.models import Patient
from medicines.models import Medicine
from django.core.validators import MinValueValidator
import phonenumbers
from django.core.exceptions import ValidationError




class OrderAddress(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

    description = models.TextField(null=True, blank=True)
    
    def validate_phone_number(value):
        try:
            phone_number = phonenumbers.parse(value)
            if not phonenumbers.is_valid_number(phone_number):
                raise ValidationError("Invalid phone number")
        except phonenumbers.phonenumberutil.NumberParseException:
            raise ValidationError("Invalid phone number")

    phone = models.CharField(max_length=255, validators=[validate_phone_number])

class Order(models.Model):
    PAYMENT_METHOD_CASH = 'COD'
    PAYMENT_METHOD_VISA = 'VIS'
    PAYMENT_METHOD_CREDIT = 'CRD'
    PAYMENT_METHOD_CHOICES = [
        (PAYMENT_METHOD_CASH, 'cash on delivery'),
        (PAYMENT_METHOD_VISA, 'visa'),
        (PAYMENT_METHOD_CREDIT, 'site credit')
    ]
    
    ORDER_STATUS_PENDING = 'PEN'
    ORDER_STATUS_CONFIRMED = 'CON'
    ORDER_STATUS_COMPLETE = 'COM'
    ORDER_STATUS_CANCELED = 'CAN'
    ORDER_STATUS_CHOICES = [
        (ORDER_STATUS_PENDING, 'Pending'),
        (ORDER_STATUS_CONFIRMED, 'Confirmed'),
        (ORDER_STATUS_COMPLETE, 'Complete'),
        (ORDER_STATUS_CANCELED, 'Canceled')
    ]
    
    

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=3, choices=PAYMENT_METHOD_CHOICES, default=PAYMENT_METHOD_CASH)
    order_status = models.CharField(max_length=3, choices=ORDER_STATUS_CHOICES, default=ORDER_STATUS_PENDING)
    customer = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.OneToOneField(OrderAddress, on_delete=models.CASCADE, related_name='order')


    class Meta:
        permissions = [('cancel_order', 'Can cancel order')]




class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Medicine, on_delete=models.PROTECT, related_name='orderitems')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='cart')

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together = [['cart', 'product']]