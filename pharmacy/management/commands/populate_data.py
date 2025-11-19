"""
Management command to populate the database with sample data.
Usage: python manage.py populate_data
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from pharmacy.models import Medicine, Order


class Command(BaseCommand):
    help = 'Populate database with sample medicines and orders'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting to populate database...')
        
        # Clear existing data (optional - comment out if you want to keep existing data)
        Order.objects.all().delete()
        Medicine.objects.all().delete()
        self.stdout.write('Cleared existing data')
        
        # Create sample medicines
        medicines_data = [
            {
                'name': 'Aspirin',
                'description': 'Pain reliever and anti-inflammatory medication',
                'price': Decimal('9.99'),
                'stock': 100,
                'expiry_date': timezone.now().date() + timedelta(days=365)
            },
            {
                'name': 'Paracetamol',
                'description': 'Fever reducer and mild pain reliever',
                'price': Decimal('12.99'),
                'stock': 150,
                'expiry_date': timezone.now().date() + timedelta(days=400)
            },
            {
                'name': 'Ibuprofen',
                'description': 'Non-steroidal anti-inflammatory drug',
                'price': Decimal('15.50'),
                'stock': 200,
                'expiry_date': timezone.now().date() + timedelta(days=500)
            },
            {
                'name': 'Vitamin C',
                'description': 'Immune system booster and antioxidant',
                'price': Decimal('18.99'),
                'stock': 180,
                'expiry_date': timezone.now().date() + timedelta(days=600)
            },
            {
                'name': 'Vitamin D',
                'description': 'Essential for bone health and immune function',
                'price': Decimal('22.50'),
                'stock': 120,
                'expiry_date': timezone.now().date() + timedelta(days=550)
            },
            {
                'name': 'Omeprazole',
                'description': 'Reduces stomach acid production',
                'price': Decimal('25.99'),
                'stock': 80,
                'expiry_date': timezone.now().date() + timedelta(days=450)
            },
            {
                'name': 'Amoxicillin',
                'description': 'Antibiotic for bacterial infections',
                'price': Decimal('30.00'),
                'stock': 60,
                'expiry_date': timezone.now().date() + timedelta(days=300)
            },
            {
                'name': 'Cetirizine',
                'description': 'Antihistamine for allergy relief',
                'price': Decimal('14.75'),
                'stock': 140,
                'expiry_date': timezone.now().date() + timedelta(days=420)
            },
            {
                'name': 'Metformin',
                'description': 'Medication for type 2 diabetes',
                'price': Decimal('28.50'),
                'stock': 90,
                'expiry_date': timezone.now().date() + timedelta(days=380)
            },
            {
                'name': 'Losartan',
                'description': 'Blood pressure medication',
                'price': Decimal('32.99'),
                'stock': 75,
                'expiry_date': timezone.now().date() + timedelta(days=400)
            }
        ]
        
        medicines = []
        for med_data in medicines_data:
            medicine = Medicine.objects.create(**med_data)
            medicines.append(medicine)
            self.stdout.write(
                self.style.SUCCESS(f'Created medicine: {medicine.name}')
            )
        
        # Create sample orders
        orders_data = [
            {
                'customer_name': 'John Doe',
                'medicine': medicines[0],  # Aspirin
                'quantity': 5
            },
            {
                'customer_name': 'Jane Smith',
                'medicine': medicines[1],  # Paracetamol
                'quantity': 3
            },
            {
                'customer_name': 'Robert Johnson',
                'medicine': medicines[2],  # Ibuprofen
                'quantity': 10
            },
            {
                'customer_name': 'Emily Davis',
                'medicine': medicines[3],  # Vitamin C
                'quantity': 2
            },
            {
                'customer_name': 'Michael Brown',
                'medicine': medicines[4],  # Vitamin D
                'quantity': 4
            },
            {
                'customer_name': 'Sarah Wilson',
                'medicine': medicines[5],  # Omeprazole
                'quantity': 1
            },
            {
                'customer_name': 'David Martinez',
                'medicine': medicines[7],  # Cetirizine
                'quantity': 6
            },
            {
                'customer_name': 'Lisa Anderson',
                'medicine': medicines[0],  # Aspirin
                'quantity': 8
            }
        ]
        
        order_statuses = ['Pending', 'Processing', 'Shipped', 'Delivered']
        
        for idx, order_data in enumerate(orders_data):
            order = Order.objects.create(**order_data)
            # Update status for some orders
            if idx % 2 == 0 and idx > 0:
                order.status = order_statuses[min(idx // 2, 3)]
                order.save()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Created order #{order.id} for {order.customer_name} - Status: {order.status}'
                )
            )
        
        # Print summary
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS('Database population completed!'))
        self.stdout.write(self.style.SUCCESS(f'Total Medicines: {Medicine.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Total Orders: {Order.objects.count()}'))
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write('')
        self.stdout.write('You can now:')
        self.stdout.write('1. Visit http://127.0.0.1:8000/ for the web interface')
        self.stdout.write('2. Visit http://127.0.0.1:8000/api/ for the API')
        self.stdout.write('3. Run tests: python manage.py test or pytest')

