"""
Views for the MediCart pharmacy application.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Medicine, Order
from .serializers import (
    MedicineSerializer,
    OrderSerializer,
    OrderStatusUpdateSerializer
)
import logging

logger = logging.getLogger(__name__)


# ==================== API Views ====================

class MedicineViewSet(viewsets.ModelViewSet):
    """
    API ViewSet for Medicine CRUD operations.
    
    Provides:
    - list: Get all medicines
    - retrieve: Get a specific medicine
    - create: Add a new medicine
    - update: Update a medicine
    - partial_update: Partially update a medicine
    - destroy: Delete a medicine
    """
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    
    def list(self, request, *args, **kwargs):
        """List all medicines with logging."""
        logger.info("Fetching all medicines")
        response = super().list(request, *args, **kwargs)
        logger.info(f"Retrieved {len(response.data)} medicines")
        return response
    
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a specific medicine with logging."""
        logger.info(f"Fetching medicine with ID: {kwargs.get('pk')}")
        return super().retrieve(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        """Create a new medicine with logging."""
        logger.info(f"Creating new medicine: {request.data.get('name')}")
        response = super().create(request, *args, **kwargs)
        logger.info(f"Medicine created successfully with ID: {response.data.get('id')}")
        return response
    
    def update(self, request, *args, **kwargs):
        """Update a medicine with logging."""
        logger.info(f"Updating medicine with ID: {kwargs.get('pk')}")
        response = super().update(request, *args, **kwargs)
        logger.info(f"Medicine updated successfully")
        return response
    
    def destroy(self, request, *args, **kwargs):
        """Delete a medicine with logging."""
        medicine_id = kwargs.get('pk')
        logger.info(f"Deleting medicine with ID: {medicine_id}")
        
        try:
            medicine = self.get_object()
            # Check if medicine has pending orders
            pending_orders = medicine.orders.filter(status='Pending').count()
            if pending_orders > 0:
                logger.warning(
                    f"Cannot delete medicine {medicine_id}: has {pending_orders} pending orders"
                )
                return Response(
                    {'detail': f'Cannot delete medicine with {pending_orders} pending orders.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            response = super().destroy(request, *args, **kwargs)
            logger.info(f"Medicine deleted successfully")
            return response
        except Exception as e:
            logger.error(f"Error deleting medicine: {str(e)}")
            raise


class OrderViewSet(viewsets.ModelViewSet):
    """
    API ViewSet for Order CRUD operations.
    
    Provides:
    - list: Get all orders
    - retrieve: Get a specific order
    - create: Place a new order
    - update: Update an order
    - partial_update: Partially update an order
    - destroy: Delete an order
    - update_status: Custom action to update order status
    """
    queryset = Order.objects.all().select_related('medicine')
    serializer_class = OrderSerializer
    
    def list(self, request, *args, **kwargs):
        """List all orders with logging."""
        logger.info("Fetching all orders")
        response = super().list(request, *args, **kwargs)
        logger.info(f"Retrieved {len(response.data)} orders")
        return response
    
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a specific order with logging."""
        logger.info(f"Fetching order with ID: {kwargs.get('pk')}")
        return super().retrieve(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        """Create a new order with logging."""
        logger.info(f"Creating new order for customer: {request.data.get('customer_name')}")
        try:
            response = super().create(request, *args, **kwargs)
            logger.info(f"Order created successfully with ID: {response.data.get('id')}")
            return response
        except Exception as e:
            logger.error(f"Error creating order: {str(e)}")
            raise
    
    def update(self, request, *args, **kwargs):
        """Update an order with logging."""
        logger.info(f"Updating order with ID: {kwargs.get('pk')}")
        response = super().update(request, *args, **kwargs)
        logger.info(f"Order updated successfully")
        return response
    
    def destroy(self, request, *args, **kwargs):
        """Delete an order with logging."""
        logger.info(f"Deleting order with ID: {kwargs.get('pk')}")
        response = super().destroy(request, *args, **kwargs)
        logger.info(f"Order deleted successfully")
        return response
    
    @action(detail=True, methods=['patch'], serializer_class=OrderStatusUpdateSerializer)
    def update_status(self, request, pk=None):
        """
        Custom action to update only the order status.
        URL: /api/orders/{id}/update_status/
        """
        order = self.get_object()
        serializer = OrderStatusUpdateSerializer(order, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Order {pk} status updated to: {serializer.data['status']}")
            return Response(serializer.data)
        
        logger.warning(f"Invalid status update for order {pk}: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ==================== Template Views ====================

def home(request):
    """Home page view."""
    medicine_count = Medicine.objects.count()
    order_count = Order.objects.count()
    low_stock_count = Medicine.objects.filter(stock__lt=10).count()
    pending_orders = Order.objects.filter(status='Pending').count()
    
    context = {
        'medicine_count': medicine_count,
        'order_count': order_count,
        'low_stock_count': low_stock_count,
        'pending_orders': pending_orders,
    }
    return render(request, 'pharmacy/home.html', context)


def medicine_list(request):
    """View to display list of all medicines."""
    medicines = Medicine.objects.all()
    
    # Pagination
    paginator = Paginator(medicines, 10)  # Show 10 medicines per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'medicines': page_obj,
    }
    return render(request, 'pharmacy/medicine_list.html', context)


def medicine_add(request):
    """View to add a new medicine."""
    if request.method == 'POST':
        try:
            # Create medicine from form data
            medicine = Medicine(
                name=request.POST.get('name'),
                description=request.POST.get('description'),
                price=request.POST.get('price'),
                stock=request.POST.get('stock'),
                expiry_date=request.POST.get('expiry_date')
            )
            medicine.full_clean()  # Validate
            medicine.save()
            
            logger.info(f"Medicine added via template: {medicine.name}")
            messages.success(request, f'Medicine "{medicine.name}" added successfully!')
            return redirect('medicine_list')
        
        except Exception as e:
            logger.error(f"Error adding medicine via template: {str(e)}")
            messages.error(request, f'Error adding medicine: {str(e)}')
    
    return render(request, 'pharmacy/medicine_add.html')


def medicine_edit(request, pk):
    """View to edit a medicine."""
    medicine = get_object_or_404(Medicine, pk=pk)
    
    if request.method == 'POST':
        try:
            medicine.name = request.POST.get('name')
            medicine.description = request.POST.get('description')
            medicine.price = request.POST.get('price')
            medicine.stock = request.POST.get('stock')
            medicine.expiry_date = request.POST.get('expiry_date')
            medicine.full_clean()
            medicine.save()
            
            logger.info(f"Medicine updated via template: {medicine.name}")
            messages.success(request, f'Medicine "{medicine.name}" updated successfully!')
            return redirect('medicine_list')
        
        except Exception as e:
            logger.error(f"Error updating medicine via template: {str(e)}")
            messages.error(request, f'Error updating medicine: {str(e)}')
    
    # Format date for HTML input
    context = {
        'medicine': medicine,
        'expiry_date': medicine.expiry_date.strftime('%Y-%m-%d')
    }
    return render(request, 'pharmacy/medicine_edit.html', context)


def medicine_delete(request, pk):
    """View to delete a medicine."""
    medicine = get_object_or_404(Medicine, pk=pk)
    
    if request.method == 'POST':
        try:
            medicine_name = medicine.name
            medicine.delete()
            logger.info(f"Medicine deleted via template: {medicine_name}")
            messages.success(request, f'Medicine "{medicine_name}" deleted successfully!')
        except Exception as e:
            logger.error(f"Error deleting medicine via template: {str(e)}")
            messages.error(request, f'Error deleting medicine: {str(e)}')
        
        return redirect('medicine_list')
    
    context = {'medicine': medicine}
    return render(request, 'pharmacy/medicine_delete.html', context)


def order_list(request):
    """View to display list of all orders."""
    orders = Order.objects.all().select_related('medicine')
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    # Pagination
    paginator = Paginator(orders, 10)  # Show 10 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'orders': page_obj,
        'status_choices': Order.STATUS_CHOICES,
        'current_status': status_filter,
    }
    return render(request, 'pharmacy/order_list.html', context)


def order_place(request):
    """View to place a new order."""
    medicines = Medicine.objects.filter(stock__gt=0)
    
    if request.method == 'POST':
        try:
            medicine_id = request.POST.get('medicine')
            medicine = get_object_or_404(Medicine, pk=medicine_id)
            quantity = int(request.POST.get('quantity'))
            
            # Create order
            order = Order(
                customer_name=request.POST.get('customer_name'),
                medicine=medicine,
                quantity=quantity
            )
            order.save()
            
            logger.info(f"Order placed via template: Order #{order.id}")
            messages.success(
                request,
                f'Order placed successfully! Order ID: {order.id}, Total: ${order.total_price}'
            )
            return redirect('order_list')
        
        except Exception as e:
            logger.error(f"Error placing order via template: {str(e)}")
            messages.error(request, f'Error placing order: {str(e)}')
    
    context = {'medicines': medicines}
    return render(request, 'pharmacy/order_place.html', context)


def order_detail(request, pk):
    """View to display order details."""
    order = get_object_or_404(Order, pk=pk)
    context = {'order': order}
    return render(request, 'pharmacy/order_detail.html', context)


def order_update_status(request, pk):
    """View to update order status."""
    order = get_object_or_404(Order, pk=pk)
    
    if request.method == 'POST':
        try:
            new_status = request.POST.get('status')
            order.status = new_status
            order.save()
            
            logger.info(f"Order status updated via template: Order #{order.id} -> {new_status}")
            messages.success(request, f'Order status updated to "{new_status}"!')
            return redirect('order_detail', pk=pk)
        
        except Exception as e:
            logger.error(f"Error updating order status via template: {str(e)}")
            messages.error(request, f'Error updating order status: {str(e)}')
    
    context = {
        'order': order,
        'status_choices': Order.STATUS_CHOICES,
    }
    return render(request, 'pharmacy/order_update_status.html', context)

