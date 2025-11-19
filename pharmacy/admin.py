"""
Admin configuration for pharmacy app.
"""
from django.contrib import admin
from .models import Medicine, Order


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    """Admin interface for Medicine model."""
    list_display = ['name', 'price', 'stock', 'expiry_date', 'is_in_stock']
    list_filter = ['expiry_date', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin interface for Order model."""
    list_display = ['id', 'customer_name', 'medicine', 'quantity', 'status', 'order_date', 'total_price']
    list_filter = ['status', 'order_date']
    search_fields = ['customer_name', 'medicine__name']
    ordering = ['-order_date']
    readonly_fields = ['order_date', 'total_price']

