"""
Comprehensive tests for the MediCart pharmacy application.
"""
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from .models import Medicine, Order


class MedicineModelTest(TestCase):
    """Test cases for Medicine model."""
    
    def setUp(self):
        """Set up test data."""
        self.medicine = Medicine.objects.create(
            name="Aspirin",
            description="Pain reliever",
            price=Decimal("9.99"),
            stock=100,
            expiry_date=timezone.now().date() + timedelta(days=365)
        )
    
    def test_medicine_creation(self):
        """Test medicine creation."""
        self.assertEqual(self.medicine.name, "Aspirin")
        self.assertEqual(self.medicine.price, Decimal("9.99"))
        self.assertEqual(self.medicine.stock, 100)
    
    def test_medicine_string_representation(self):
        """Test __str__ method."""
        expected = f"Aspirin - $9.99"
        self.assertEqual(str(self.medicine), expected)
    
    def test_is_in_stock(self):
        """Test is_in_stock method."""
        self.assertTrue(self.medicine.is_in_stock())
        
        self.medicine.stock = 0
        self.assertFalse(self.medicine.is_in_stock())
    
    def test_negative_stock_validation(self):
        """Test that negative stock raises error."""
        from django.core.exceptions import ValidationError
        medicine = Medicine(
            name="Test Medicine",
            description="Test",
            price=Decimal("10.00"),
            stock=-5,
            expiry_date=timezone.now().date() + timedelta(days=30)
        )
        with self.assertRaises(ValidationError):
            medicine.full_clean()


class OrderModelTest(TestCase):
    """Test cases for Order model."""
    
    def setUp(self):
        """Set up test data."""
        self.medicine = Medicine.objects.create(
            name="Ibuprofen",
            description="Anti-inflammatory",
            price=Decimal("15.50"),
            stock=50,
            expiry_date=timezone.now().date() + timedelta(days=365)
        )
    
    def test_order_creation(self):
        """Test order creation and stock reduction."""
        initial_stock = self.medicine.stock
        
        order = Order.objects.create(
            customer_name="John Doe",
            medicine=self.medicine,
            quantity=5
        )
        
        self.assertEqual(order.customer_name, "John Doe")
        self.assertEqual(order.quantity, 5)
        self.assertEqual(order.status, "Pending")
        self.assertEqual(order.total_price, Decimal("77.50"))
        
        # Check stock was reduced
        self.medicine.refresh_from_db()
        self.assertEqual(self.medicine.stock, initial_stock - 5)
    
    def test_order_string_representation(self):
        """Test __str__ method."""
        order = Order.objects.create(
            customer_name="Jane Smith",
            medicine=self.medicine,
            quantity=2
        )
        expected = f"Order #{order.id} - Jane Smith"
        self.assertEqual(str(order), expected)
    
    def test_insufficient_stock(self):
        """Test order with insufficient stock."""
        from django.core.exceptions import ValidationError
        
        with self.assertRaises(ValidationError):
            Order.objects.create(
                customer_name="Test User",
                medicine=self.medicine,
                quantity=100  # More than available stock
            )
    
    def test_order_deletion_restores_stock(self):
        """Test that deleting pending order restores stock."""
        initial_stock = self.medicine.stock
        
        order = Order.objects.create(
            customer_name="Test User",
            medicine=self.medicine,
            quantity=10
        )
        
        self.medicine.refresh_from_db()
        self.assertEqual(self.medicine.stock, initial_stock - 10)
        
        order.delete()
        
        self.medicine.refresh_from_db()
        self.assertEqual(self.medicine.stock, initial_stock)


class MedicineAPITest(APITestCase):
    """Test cases for Medicine API endpoints."""
    
    def setUp(self):
        """Set up test data and API client."""
        self.client = APIClient()
        self.medicine_data = {
            'name': 'Paracetamol',
            'description': 'Fever reducer',
            'price': '12.99',
            'stock': 200,
            'expiry_date': (timezone.now().date() + timedelta(days=365)).isoformat()
        }
        self.medicine = Medicine.objects.create(
            name="Aspirin",
            description="Pain reliever",
            price=Decimal("9.99"),
            stock=100,
            expiry_date=timezone.now().date() + timedelta(days=365)
        )
    
    def test_get_all_medicines(self):
        """Test retrieving all medicines."""
        url = reverse('medicine-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_get_single_medicine(self):
        """Test retrieving a single medicine."""
        url = reverse('medicine-detail', args=[self.medicine.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Aspirin')
    
    def test_create_medicine(self):
        """Test creating a new medicine."""
        url = reverse('medicine-list')
        response = self.client.post(url, self.medicine_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Medicine.objects.count(), 2)
        self.assertEqual(response.data['name'], 'Paracetamol')
    
    def test_create_medicine_with_past_expiry_date(self):
        """Test creating medicine with past expiry date fails."""
        url = reverse('medicine-list')
        invalid_data = self.medicine_data.copy()
        invalid_data['expiry_date'] = (timezone.now().date() - timedelta(days=1)).isoformat()
        
        response = self.client.post(url, invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update_medicine(self):
        """Test updating a medicine."""
        url = reverse('medicine-detail', args=[self.medicine.id])
        updated_data = {
            'name': 'Aspirin Updated',
            'description': 'Updated description',
            'price': '11.99',
            'stock': 150,
            'expiry_date': (timezone.now().date() + timedelta(days=400)).isoformat()
        }
        response = self.client.put(url, updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.medicine.refresh_from_db()
        self.assertEqual(self.medicine.name, 'Aspirin Updated')
        self.assertEqual(self.medicine.stock, 150)
    
    def test_partial_update_medicine(self):
        """Test partially updating a medicine."""
        url = reverse('medicine-detail', args=[self.medicine.id])
        partial_data = {'stock': 75}
        response = self.client.patch(url, partial_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.medicine.refresh_from_db()
        self.assertEqual(self.medicine.stock, 75)
    
    def test_delete_medicine(self):
        """Test deleting a medicine."""
        url = reverse('medicine-detail', args=[self.medicine.id])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Medicine.objects.count(), 0)
    
    def test_delete_medicine_with_pending_orders(self):
        """Test that medicine with pending orders cannot be deleted."""
        # Create a pending order
        Order.objects.create(
            customer_name="Test User",
            medicine=self.medicine,
            quantity=5
        )
        
        url = reverse('medicine-detail', args=[self.medicine.id])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Medicine.objects.count(), 1)


class OrderAPITest(APITestCase):
    """Test cases for Order API endpoints."""
    
    def setUp(self):
        """Set up test data and API client."""
        self.client = APIClient()
        self.medicine = Medicine.objects.create(
            name="Vitamin C",
            description="Immune booster",
            price=Decimal("20.00"),
            stock=100,
            expiry_date=timezone.now().date() + timedelta(days=365)
        )
        self.order_data = {
            'customer_name': 'Alice Johnson',
            'medicine': self.medicine.id,
            'quantity': 3
        }
    
    def test_get_all_orders(self):
        """Test retrieving all orders."""
        Order.objects.create(
            customer_name="Test User",
            medicine=self.medicine,
            quantity=5
        )
        
        url = reverse('order-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_get_single_order(self):
        """Test retrieving a single order."""
        order = Order.objects.create(
            customer_name="Test User",
            medicine=self.medicine,
            quantity=5
        )
        
        url = reverse('order-detail', args=[order.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['customer_name'], 'Test User')
    
    def test_create_order(self):
        """Test creating a new order."""
        url = reverse('order-list')
        response = self.client.post(url, self.order_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        
        # Check stock was reduced
        self.medicine.refresh_from_db()
        self.assertEqual(self.medicine.stock, 97)
    
    def test_create_order_insufficient_stock(self):
        """Test creating order with insufficient stock."""
        url = reverse('order-list')
        invalid_data = self.order_data.copy()
        invalid_data['quantity'] = 150  # More than available
        
        response = self.client.post(url, invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)
    
    def test_update_order_status(self):
        """Test updating order status."""
        order = Order.objects.create(
            customer_name="Test User",
            medicine=self.medicine,
            quantity=5
        )
        
        url = reverse('order-update-status', args=[order.id])
        status_data = {'status': 'Delivered'}
        response = self.client.patch(url, status_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertEqual(order.status, 'Delivered')
    
    def test_delete_order(self):
        """Test deleting an order."""
        initial_stock = self.medicine.stock
        
        order = Order.objects.create(
            customer_name="Test User",
            medicine=self.medicine,
            quantity=10
        )
        
        url = reverse('order-detail', args=[order.id])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), 0)
        
        # Check stock was restored
        self.medicine.refresh_from_db()
        self.assertEqual(self.medicine.stock, initial_stock)


class TemplateViewTest(TestCase):
    """Test cases for template views."""
    
    def setUp(self):
        """Set up test data and client."""
        self.client = Client()
        self.medicine = Medicine.objects.create(
            name="Test Medicine",
            description="Test description",
            price=Decimal("25.00"),
            stock=50,
            expiry_date=timezone.now().date() + timedelta(days=365)
        )
    
    def test_home_page(self):
        """Test home page loads correctly."""
        url = reverse('home')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'MediCart')
    
    def test_medicine_list_page(self):
        """Test medicine list page."""
        url = reverse('medicine_list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Medicine')
    
    def test_medicine_add_page_get(self):
        """Test medicine add page GET request."""
        url = reverse('medicine_add')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Add New Medicine')
    
    def test_medicine_add_page_post(self):
        """Test medicine add page POST request."""
        url = reverse('medicine_add')
        data = {
            'name': 'New Medicine',
            'description': 'New description',
            'price': '30.00',
            'stock': 75,
            'expiry_date': (timezone.now().date() + timedelta(days=365)).isoformat()
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertEqual(Medicine.objects.filter(name='New Medicine').count(), 1)
    
    def test_order_list_page(self):
        """Test order list page."""
        Order.objects.create(
            customer_name="Test Customer",
            medicine=self.medicine,
            quantity=5
        )
        
        url = reverse('order_list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Customer')
    
    def test_order_place_page_get(self):
        """Test order place page GET request."""
        url = reverse('order_place')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Place New Order')
    
    def test_order_place_page_post(self):
        """Test order place page POST request."""
        url = reverse('order_place')
        data = {
            'customer_name': 'New Customer',
            'medicine': self.medicine.id,
            'quantity': 3
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertEqual(Order.objects.filter(customer_name='New Customer').count(), 1)
    
    def test_order_detail_page(self):
        """Test order detail page."""
        order = Order.objects.create(
            customer_name="Detail Test",
            medicine=self.medicine,
            quantity=2
        )
        
        url = reverse('order_detail', args=[order.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Detail Test')
        self.assertContains(response, f'Order #{order.id}')

