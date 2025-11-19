"""
Models for the MediCart pharmacy application.
"""
from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)


class Medicine(models.Model):
    """Model representing a medicine in the pharmacy."""
    
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    stock = models.IntegerField(validators=[MinValueValidator(0)])
    expiry_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Medicine'
        verbose_name_plural = 'Medicines'
    
    def __str__(self):
        return f"{self.name} - ${self.price}"
    
    def is_in_stock(self):
        """Check if medicine is in stock."""
        return self.stock > 0
    
    def clean(self):
        """Validate model fields."""
        from django.utils import timezone
        if self.expiry_date and self.expiry_date < timezone.now().date():
            raise ValidationError('Expiry date cannot be in the past.')


class Order(models.Model):
    """Model representing an order in the pharmacy."""
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    
    customer_name = models.CharField(max_length=200)
    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.PROTECT,
        related_name='orders'
    )
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        editable=False,
        null=True
    )
    
    class Meta:
        ordering = ['-order_date']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
    
    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"
    
    def save(self, *args, **kwargs):
        """Override save to update stock and calculate total price."""
        is_new = self.pk is None
        
        if is_new:
            # Check if medicine has enough stock
            if self.medicine.stock < self.quantity:
                logger.warning(
                    f"Insufficient stock for {self.medicine.name}. "
                    f"Available: {self.medicine.stock}, Requested: {self.quantity}"
                )
                raise ValidationError(
                    f"Insufficient stock. Only {self.medicine.stock} units available."
                )
            
            # Calculate total price
            self.total_price = self.medicine.price * self.quantity
            
            # Save the order first
            super().save(*args, **kwargs)
            
            # Reduce stock
            self.medicine.stock -= self.quantity
            self.medicine.save()
            
            logger.info(
                f"New order created: {self.id} for {self.customer_name}. "
                f"Medicine: {self.medicine.name}, Quantity: {self.quantity}"
            )
        else:
            # For updates, just save
            super().save(*args, **kwargs)
            logger.info(f"Order {self.id} updated. Status: {self.status}")
    
    def delete(self, *args, **kwargs):
        """Override delete to restore stock."""
        # Restore stock when order is deleted
        if self.status == 'Pending':
            self.medicine.stock += self.quantity
            self.medicine.save()
            logger.info(
                f"Order {self.id} deleted. Stock restored for {self.medicine.name}"
            )
        super().delete(*args, **kwargs)

