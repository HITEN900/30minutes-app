from django.db import models
from django.conf import settings
from services.models import Service

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('rejected', 'Rejected'),
    )
    
    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )
    
    PAYMENT_METHODS = (
        ('upi', 'UPI'),
        ('card', 'Card'),
        ('wallet', 'Wallet'),
        ('cash', 'Cash'),
    )
    
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer_bookings')
    technician = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='technician_bookings')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings', null=True, blank=True)
    
    # Direct fields for booking
    service_type = models.CharField(max_length=50, default='general')
    description = models.TextField(blank=True, null=True)
    address = models.TextField()
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    scheduled_time = models.DateTimeField()
    estimated_arrival = models.IntegerField(default=30)
    actual_arrival = models.IntegerField(null=True, blank=True)
    
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, null=True, blank=True)
    
    technician_notes = models.TextField(null=True, blank=True)
    customer_notes = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f'Booking #{self.id} - {self.customer.email}'
    
    def get_total_duration(self):
        if self.completed_at and self.updated_at:
            return (self.completed_at - self.updated_at).total_seconds() / 60
        return None
    
    class Meta:
        db_table = 'bookings'
        ordering = ['-created_at']
