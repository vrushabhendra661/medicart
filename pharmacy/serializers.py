"""
Serializers for the MediCart pharmacy application.
"""
from rest_framework import serializers
from .models import Medicine, Order
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


class MedicineSerializer(serializers.ModelSerializer):
    """Serializer for Medicine model."""
    
    is_in_stock = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Medicine
        fields = [
            'id', 'name', 'description', 'price', 'stock',
            'expiry_date', 'is_in_stock', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_expiry_date(self, value):
        """Validate that expiry date is not in the past."""
        if value < timezone.now().date():
            logger.warning(f"Attempted to create medicine with past expiry date: {value}")
            raise serializers.ValidationError("Expiry date cannot be in the past.")
        return value
    
    def validate_price(self, value):
        """Validate price is positive."""
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value
    
    def validate_stock(self, value):
        """Validate stock is not negative."""
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return value


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order model."""
    
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)
    medicine_price = serializers.DecimalField(
        source='medicine.price',
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    
    class Meta:
        model = Order
        fields = [
            'id', 'customer_name', 'medicine', 'medicine_name',
            'medicine_price', 'quantity', 'order_date', 'status', 'total_price'
        ]
        read_only_fields = ['id', 'order_date', 'total_price']
    
    def validate_quantity(self, value):
        """Validate quantity is positive."""
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0.")
        return value
    
    def validate(self, data):
        """Validate that medicine has enough stock."""
        medicine = data.get('medicine')
        quantity = data.get('quantity')
        
        if medicine and quantity:
            if medicine.stock < quantity:
                logger.warning(
                    f"Order validation failed: Insufficient stock for {medicine.name}"
                )
                raise serializers.ValidationError({
                    'quantity': f"Insufficient stock. Only {medicine.stock} units available."
                })
        
        return data


class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating order status only."""
    
    class Meta:
        model = Order
        fields = ['status']
    
    def validate_status(self, value):
        """Validate status is a valid choice."""
        valid_statuses = [choice[0] for choice in Order.STATUS_CHOICES]
        if value not in valid_statuses:
            raise serializers.ValidationError(
                f"Invalid status. Choose from: {', '.join(valid_statuses)}"
            )
        return value

